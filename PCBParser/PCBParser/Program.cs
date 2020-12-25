using System;
using System.Collections.Generic;
using System.Data;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Linq.Expressions;
using System.Net;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading;
using System.Threading.Tasks;
using ExcelDataReader;
using System.Globalization;
using System.IO.Compression;
using System.Reflection;

namespace PCBParser
{
    class Program
    {
        const bool update_data = true;
        const bool update_prices = false;
        const string api_username = "qwer";
        const string api_password = "qwer";

        const string cpu_url = "https://www.userbenchmark.com/resources/download/csv/CPU_UserBenchmarks.csv";
        const string gpu_url = "https://www.userbenchmark.com/resources/download/csv/GPU_UserBenchmarks.csv";
        const string ram_url = "https://www.userbenchmark.com/resources/download/csv/RAM_UserBenchmarks.csv";
        const string ssd_url = "https://www.userbenchmark.com/resources/download/csv/SSD_UserBenchmarks.csv";
        const string hdd_url = "https://www.userbenchmark.com/resources/download/csv/HDD_UserBenchmarks.csv";
        const string motherboard_url = "https://motherboarddb.com/motherboards/ajax/table/?dt=table&page=";
        const string specs_url = "https://www.overclockers.ua/specs/";

        static readonly (string, string)[] dnsUrls =
        {
            ("Moscow", "https://www.dns-shop.ru/files/price/price-moscow.zip"),
            ("St. Petersburg", "https://www.dns-shop.ru/files/price/price-spb.zip"),
            ("Novosibirsk", "https://www.dns-shop.ru/files/price/price-novosibirsk.zip"),
            ("Ekaterinburg", "https://www.dns-shop.ru/files/price/price-ekaterinburg.zip")
        };

        const string data_path = "data\\";
        const int components_index = 4;
        const int name_index = 1;

        static async Task Main(string[] args)
        {
            if (!Directory.Exists(data_path))
                Directory.CreateDirectory(data_path);

            if (!Server.LogIn(api_username, api_password))
            {
                ConsoleLog("Could not connect/login to the server");
                Console.ReadKey();
                return;
            }
            ConsoleLog("Authorization was successful");

            DateTime startTime = DateTime.Now;

            List<List<ComponentPrice>> allPrices = new List<List<ComponentPrice>>();
            Task priceParserTask = Task.Run(() => Parallel.For(0, dnsUrls.Length, (i) =>
            {
                ConsoleLog($"Downloading {dnsUrls[i].Item1} prices");
                if (!File.Exists($"{data_path}prices{i}.xls") || update_prices)
                {
                    WebClient webClient = new WebClient();
                    webClient.Headers.Add("user-agent", "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; .NET CLR 1.0.3705;)");
                    webClient.DownloadFile(dnsUrls[i].Item2, $"{data_path}prices{i}.zip");

                    ConsoleLog("Extracting prices");
                    using (ZipArchive zipArchive = ZipFile.OpenRead($"{data_path}prices{i}.zip"))
                        zipArchive.Entries[0].ExtractToFile($"{data_path}prices{i}.xls", true);
                }
                ConsoleLog("Parsing prices");
                List<ComponentPrice> tempPrices = ParsePrices($"{data_path}prices{i}.xls");
                allPrices.Add(tempPrices);
                ConsoleLog($"Parsing done, {tempPrices.Count} prices");
            }));

            ConsoleLog("Downloading specifications");
            if (!File.Exists($"{data_path}specs.txt") || update_data)
                new WebClient().DownloadFile(specs_url, $"{data_path}specs.txt");

            ConsoleLog("Parsing specifications");
            Task<List<Specification>> specificationsTask = Task.Run(() => ParseSpecifications($"{data_path}specs.txt"));

            ConsoleLog("Downloading options");
            OptionCollection options = new OptionCollection
            {
                Brands = Server.DownloadInfo<Brand>(),
                Sockets = Server.DownloadInfo<Socket>(),
                MemoryTypes = Server.DownloadInfo<MemoryType>(),
                Chipsets = Server.DownloadInfo<Chipset>(),
                Formfactors = Server.DownloadInfo<Formfactor>(),
            };
            ConsoleLog($"Done, {options.Brands.Count} brands, {options.Sockets.Count} sockets, " +
                $"{options.MemoryTypes.Count} memory types, {options.Chipsets.Count} chipsets, " +
                $"{options.Formfactors.Count} formfactors loaded");

            ConsoleLog("Downloading components");
            List<PowerSupply> powerSupplies = Server.DownloadInfo<PowerSupply>();
            List<MotherBoard> motherBoards = Server.DownloadInfo<MotherBoard>();
            List<CPU> cpus = Server.DownloadInfo<CPU>();
            List<GPU> gpus = Server.DownloadInfo<GPU>();
            List<RAM> rams = Server.DownloadInfo<RAM>();
            List<SSD> ssds = Server.DownloadInfo<SSD>();
            List<HDD> hdds = Server.DownloadInfo<HDD>();
            ConsoleLog($"Done, {motherBoards.Count} motherboards, {cpus.Count} CPUs, {gpus.Count} GPUs, " +
                $"{rams.Count} RAMs, {ssds.Count} SSDs, {hdds.Count} HDDs, {powerSupplies.Count} power supplies loaded");

            List<Specification> specifications = await specificationsTask;
            ConsoleLog($"Parsing done, {specifications.Count} specifications");

            await priceParserTask;
            ConsoleLog("Combining prices");
            List<ComponentPrice> prices = CombinePrices(allPrices);
            ConsoleLog($"Combining done, {prices.Count} prices");

            Task<List<PowerSupply>> powerSuppliesTask = ParsePowerSuppliesAsync(powerSupplies, prices, options);
            Task<List<MotherBoard>> motherBoardsFirstTask = ParseMotherBoardsAsync(motherBoards, prices, options, false);
            Task<List<MotherBoard>> motherBoardsSecondTask = ParseMotherBoardsAsync(motherBoards, prices, options, true);
            Task<List<CPU>> cpusTask = ParseComponentsAsync(cpu_url, cpus, prices, options, new CPU());
            Task<List<GPU>> gpusTask = ParseComponentsAsync(gpu_url, gpus, prices, options, new GPU());
            Task<List<RAM>> ramsTask = ParseComponentsAsync(ram_url, rams, prices, options, new RAM());
            Task<List<SSD>> ssdsTask = ParseComponentsAsync(ssd_url, ssds, prices, options, new SSD());
            Task<List<HDD>> hddsTask = ParseComponentsAsync(hdd_url, hdds, prices, options, new HDD());

            Task uploadRam = UploadComponentsAsync(await ramsTask);
            Task uploadPs = UploadComponentsAsync(await powerSuppliesTask);

            cpusTask = GetSpecificationsAsync(await cpusTask, specifications, options);
            gpusTask = GetSpecificationsAsync(await gpusTask, specifications, options);
            Task uploadSsd = UploadComponentsAsync(await ssdsTask);
            Task uploadHdd = UploadComponentsAsync(await hddsTask);

            Task uploadGpu = UploadComponentsAsync(await gpusTask);
            Task uploadMb1 = UploadComponentsAsync(await motherBoardsFirstTask);
            Task uploadMb2 = UploadComponentsAsync(await motherBoardsSecondTask);
            Task uploadCpu = UploadComponentsAsync(await cpusTask);
            await Task.WhenAll(uploadCpu, uploadGpu, uploadRam, uploadSsd, uploadHdd, uploadMb1, uploadMb2, uploadPs);

            TimeSpan resultTime = DateTime.Now - startTime;
            ConsoleLog($"Parsing done in {resultTime}");

            Console.ReadKey();
        }

        static async Task<List<PowerSupply>> ParsePowerSuppliesAsync(List<PowerSupply> powerSupplies,
            List<ComponentPrice> prices, OptionCollection options)
        {
            return await Task.Run(() => CParsePowerSupplies(powerSupplies, prices, options));
        }

        static async Task<List<MotherBoard>> ParseMotherBoardsAsync(List<MotherBoard> motherBoards, 
            List<ComponentPrice> prices, OptionCollection options, bool secondHalf)
        {
            return await Task.Run(() => CParseMotherBoards(motherBoards, prices, options, secondHalf));
        }

        static async Task<List<T>> ParseComponentsAsync<T>(string url, List<T> components,
            List<ComponentPrice> prices, OptionCollection options, T plug) where T : IComponent
        {
            return await Task.Run(() => CParseComponents(url, components, prices, options, plug));
        }

        static async Task<List<T>> GetSpecificationsAsync<T>(List<T> components,
            List<Specification> specifications, OptionCollection options) where T : IComplexComponent
        {
            return await Task.Run(() => CGetSpecifications(components, specifications, options));
        }

        static async Task UploadComponentsAsync<T>(List<T> components)
        {
            await Task.Run(() => CUploadComponents(components));
        }

        static List<PowerSupply> CParsePowerSupplies(List<PowerSupply> powerSupplies,
            List<ComponentPrice> prices, OptionCollection options)
        {
            ConsoleLog("Parsing power supplies");
            List<PowerSupply> newPowerSupplies = ParsePowerSupplies(powerSupplies, prices, options);
            ConsoleLog($"Parsing done, {newPowerSupplies.Count} new power supplies");

            return newPowerSupplies;
        }

        static List<MotherBoard> CParseMotherBoards(List<MotherBoard> motherBoards, 
            List<ComponentPrice> prices, OptionCollection options, bool secondHalf)
        {
            ConsoleLog("Parsing motherboards");
            List<MotherBoard> newMotherBoards = ParseMotherBoards(motherBoards, prices, options, secondHalf);
            ConsoleLog($"Parsing done, {newMotherBoards.Count} new motherboards");

            return newMotherBoards;
        }

        static List<T> CParseComponents<T>(string url, List<T> components, 
            List<ComponentPrice> prices, OptionCollection options, T plug) where T : IComponent
        {
            WebClient webClient = new WebClient();

            ConsoleLog($"Downloading {typeof(T).Name}s");
            if (!File.Exists($"{data_path}{typeof(T).Name}s.txt") || update_data)
                webClient.DownloadFile(url, $"{data_path}{typeof(T).Name}s.txt");

            ConsoleLog($"Parsing {typeof(T).Name}s");
            List<T> newComponents = ParseComponents($"{data_path}{typeof(T).Name}s.txt", components, prices, options, plug);
            ConsoleLog($"Parsing done, {newComponents.Count} new {typeof(T).Name}s");

            return newComponents;
        }

        static List<T> CGetSpecifications<T>(List<T> components, 
            List<Specification> specifications, OptionCollection options) where T : IComplexComponent
        {
            ConsoleLog($"Get {typeof(T).Name}s specifications");
            List<T> newComponents = GetSpecifications(components, specifications, options);
            ConsoleLog($"Done, total received {newComponents.Count} {typeof(T).Name}s specifications");
            return newComponents;
        }

        static void CUploadComponents<T>(List<T> components)
        {
            ConsoleLog($"Uploading {typeof(T).Name}s");
            int count = UploadComponents(components);
            ConsoleLog($"Done, total added {count} {typeof(T).Name}s");
        }

        public static void ConsoleLog(string message) =>
            Console.WriteLine($"{DateTime.Now.ToLongTimeString()}: {message}");

        static List<ComponentPrice> ParsePrices(string fileName)
        {
            Encoding.RegisterProvider(CodePagesEncodingProvider.Instance);

            DataSet data;
            using (FileStream file = File.OpenRead(fileName))
            using (IExcelDataReader reader = ExcelReaderFactory.CreateReader(file))
                data = reader.AsDataSet();

            DataRowCollection rows = data.Tables[components_index].Rows;
            List<ComponentPrice> prices = new List<ComponentPrice>();
            int priceIndex = -1;
            for (int i = 0; i < rows.Count; i++)
            {
                object[] items = rows[i].ItemArray;
                if (priceIndex == -1)
                {
                    for (int j = 0; j < items.Length; j++)
                    {
                        if (items[j].ToString().Contains("Цена"))
                        {
                            priceIndex = j;
                            break;
                        }
                    }
                }
                else
                {
                    string name = items[name_index].ToString();
                    string price = items[priceIndex].ToString();
                    if (name.Length > 0 && price.Length > 0)
                    {
                        if (int.TryParse(price, out int _price))
                            prices.Add(new ComponentPrice 
                            { 
                                ComponentName = name, 
                                LowerComponentName = name.ToLower(), 
                                Price = _price 
                            });
                    }
                }
            }
            data.Dispose();
            return prices;
        }

        static List<ComponentPrice> CombinePrices(List<List<ComponentPrice>> prices)
        {
            List<ComponentPrice> result = new List<ComponentPrice>();
            for (int i = 0; i < prices.Count; i++)
            {
                foreach (ComponentPrice componentPrice in prices[i])
                {
                    ComponentPrice price = result.Find(c => c.LowerComponentName == componentPrice.LowerComponentName);
                    if (price == null)
                        result.Add(componentPrice);
                }
            }
            return result;
        }

        static List<Specification> ParseSpecifications(string fileName)
        {
            Regex regex = new Regex("(<li>|<li class=\"first\">)<a href=\"(.+)\">(.+)</a></li>");
            string specs = File.ReadAllText(fileName);
            int begin = specs.IndexOf("<div id=\"spec\">");
            int end = specs.IndexOf("Сравнение видеокарт");
            specs = specs[begin..end];
            MatchCollection matches = regex.Matches(specs);
            List<Specification> specifications = new List<Specification>();
            foreach (Match match in matches)
            {
                GroupCollection groups = match.Groups;
                specifications.Add(new Specification
                {
                    Name = groups[3].Value.ToLower(),
                    Url = $"https://www.overclockers.ua{groups[2].Value}"
                });
            }
            return specifications;
        }

        static List<MotherBoard> ParseMotherBoards(List<MotherBoard> motherBoards, List<ComponentPrice> prices, OptionCollection options, bool secondHalf)
        {
            WebClient webClient = new WebClient();
            webClient.Headers.Add("user-agent", "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; .NET CLR 1.0.3705;)");

            Regex nextPageRegex = new Regex("data-page=\"(\\d+)\">Next</a>");
            Regex infoRegex = new Regex(">([^<]+)[^t]*</td>");
            Regex hrefRegex = new Regex("href=\"(.*)\"");

            List<MotherBoard> newMotherBoards = new List<MotherBoard>();
            int nextPage = 1;
            if (secondHalf)
                nextPage = 20;
            while (nextPage > 0)
            {
                string page = webClient.DownloadString($"{motherboard_url}{nextPage}");
                GroupCollection groups = nextPageRegex.Match(page).Groups;
                if (groups.Count < 2)
                    nextPage = -1;
                else
                    nextPage = int.Parse(groups[1].Value);

                if (!secondHalf && nextPage == 20)
                    nextPage = -1;

                string[] rows = page.Split("<tr>");
                for (int i = 0; i < rows.Length; i++)
                {
                    MatchCollection matches = infoRegex.Matches(rows[i].Replace("\r", "").Replace("\n", ""));
                    if (matches.Count > 0)
                    {
                        string url = "https://motherboarddb.com" + hrefRegex.Match(rows[i]).Groups[1].Value;
                        string name = matches[0].Groups[1].Value;
                        int year = int.Parse(matches[1].Groups[1].Value);
                        string socketTitle = matches[2].Groups[1].Value.Substring(3).Trim();
                        string chipsetTitle = matches[3].Groups[1].Value;
                        string formfactorTitle = matches[4].Groups[1].Value;

                        int splitIndex = name.IndexOf(' ');
                        string brandTitle = name.Remove(splitIndex);
                        string model = name.Substring(splitIndex + 1);

                        MotherBoard mb = motherBoards.Find(c => c.Model == model);
                        if (mb != null)
                            continue;

                        foreach (ComponentPrice price in prices)
                        {
                            if (price.LowerComponentName.Contains("материнская плата") &&
                                price.LowerComponentName.Contains(model.ToLower()))
                            {
                                Brand brand = Server.FindOrAdd(brandTitle, options.Brands, new Brand());
                                Socket socket = Server.FindOrAdd(socketTitle, options.Sockets, new Socket());
                                Chipset chipset = Server.FindOrAdd(chipsetTitle, options.Chipsets, new Chipset());
                                Formfactor formfactor = Server.FindOrAdd(formfactorTitle, options.Formfactors, new Formfactor());
                                newMotherBoards.Add(new MotherBoard
                                {
                                    Brand = brand.Id,
                                    Model = model,
                                    Price = price.Price,
                                    Formfactor = formfactor.Id,
                                    Chipset = chipset.Id,
                                    Socket = socket.Id,
                                    Year = year,
                                    Url = url
                                });
                                break;
                            }
                        }
                    }
                }
                ConsoleLog($"{(nextPage > 0 ? (nextPage - 1).ToString() : "last")} motherboards page parsed");
            }
            return newMotherBoards;
        }

        static List<PowerSupply> ParsePowerSupplies(List<PowerSupply> powerSupplies, List<ComponentPrice> prices, OptionCollection options)
        {
            Regex bracketRegex = new Regex(@" \[.+\]");
            Regex powerRegex = new Regex(@"[ -]\d+W");
            List<PowerSupply> newPowerSupplies = new List<PowerSupply>();
            foreach (ComponentPrice price in prices)
            {
                if (price.ComponentName.Contains("Блок питания "))
                {
                    string name = price.ComponentName.Replace("Блок питания ", "");
                    Match powerMatch = powerRegex.Match(name);
                    if (!powerMatch.Success)
                        continue;
                    string power = powerMatch.Value;
                    name = name.Replace(power, "");

                    Match bracketMatch = bracketRegex.Match(name);
                    if (bracketMatch.Success)
                        name = name.Replace(bracketMatch.Value, "");

                    string model = "";
                    int brandIndex = name.IndexOf(' ');
                    if (brandIndex > 0)
                    {
                        if (name.Contains("be "))
                            brandIndex = name.IndexOf(' ', brandIndex + 1);
                        model = name.Substring(brandIndex + 1);
                        name = name.Remove(brandIndex);
                    }
                    string brandTitle = name[0] + name.ToLower()[1..];
                    Brand brand = Server.FindOrAdd(brandTitle, options.Brands, new Brand());
                    newPowerSupplies.Add(new PowerSupply
                    {
                        Brand = brand.Id,
                        Model = model,
                        Price = price.Price,
                        Power = int.Parse(power.Replace("W", "").Replace("-", ""))
                    });
                }
            }
            return newPowerSupplies;
        }

        static List<T> ParseComponents<T>(string fileName, List<T> components, 
            List<ComponentPrice> prices, OptionCollection options, T plug) where T : IComponent
        {
            string[] file = File.ReadAllLines(fileName);
            ConsoleLog($"Table loaded, {file.Length - 1} {typeof(T).Name}s for parsing");
            List<T> newComponents = new List<T>();
            for (int i = 1; i < file.Length; i++)
            {
                string[] info = file[i].Split(',');
                string brandTitle = info[2];
                string model = info[3];
                string benchmark = info[5];
                string url = info[7];

                if (brandTitle.Length == 0)
                    continue;
                if (model.Contains(brandTitle))
                    continue;

                dynamic modelParserResult = plug.ModelParser(model);
                if (modelParserResult == null)
                    continue;

                T component = components.Find(c => c.RepeatComparer(modelParserResult));
                if (component != null)
                    continue;
                component = newComponents.Find(c => c.RepeatComparer(modelParserResult));
                if (component != null)
                    continue;

                int totalPrice = 0, countPrices = 0;
                foreach (ComponentPrice price in prices)
                {
                    if (plug.PriceComparer(price.LowerComponentName, modelParserResult))
                    {
                        totalPrice += price.Price;
                        countPrices++;
                    }
                }
                if (countPrices > 0)
                {
                    Brand brand = Server.FindOrAdd(brandTitle, options.Brands, new Brand());
                    plug.Brand = brand.Id;
                    plug.Benchmark = double.Parse(benchmark, CultureInfo.InvariantCulture);
                    plug.Price = totalPrice / countPrices;
                    plug.Url = url;
                    newComponents.Add(plug.Constructor(options, modelParserResult));
                }
            }
            return newComponents;
        }

        static List<T> GetSpecifications<T>(List<T> components,
            List<Specification> specifications, OptionCollection options) where T : IComplexComponent
        {
            WebClient webClient = new WebClient();
            webClient.Headers.Add("user-agent", "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; .NET CLR 1.0.3705;)");
            int i = 0;
            List<T> newComponents = new List<T>();
            foreach (T component in components)
            {
                foreach (Specification spec in specifications)
                {
                    if (spec.Name.Replace("geforce", "").Replace("radeon", "").Trim() == component.Model.ToLower())
                    {
                        string specification = webClient.DownloadString(spec.Url);
                        IComplexComponent newComponent = component.SpecificationParser(specification, options);
                        if (newComponent == null)
                            break;
                        newComponents.Add((T)newComponent);
                        ConsoleLog($"{i + 1} {typeof(T).Name} specification added");
                        i++;
                        break;
                    }
                }
            }
            return newComponents;
        }

        static int UploadComponents<T>(List<T> components)
        {
            Parallel.For(0, components.Count, (i) =>
            {
                Server.UploadInfo(components[i]);
                ConsoleLog($"{i + 1} {typeof(T).Name} added");
            });
            return components.Count;
        }
    }
}