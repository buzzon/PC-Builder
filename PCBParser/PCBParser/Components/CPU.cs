using System.Text.RegularExpressions;

namespace PCBParser
{
    class CPU : IComplexComponent
    {
        public int Brand { get; set; }
        public string Model { get; set; }
        public double Benchmark { get; set; }
        public int Price { get; set; }
        public string Url { get; set; }

        public int Socket { get; set; }
        public int Cores { get; set; }
        public int Threads { get; set; }
        public int Frequency { get; set; }

        public dynamic ModelParser(string model)
        {
            return new
            {
                Model = model,
                ComparerModel = $"{model.ToLower()} box"
            };
        }

        public bool RepeatComparer(dynamic modelParserResult) =>
            Model == modelParserResult.Model;

        public bool PriceComparer(string componentName, dynamic modelParserResult) =>
            componentName.Contains("процессор") &&
            componentName.Contains(modelParserResult.ComparerModel);

        public IComponent Constructor(OptionCollection options, dynamic modelParserResult)
        {
            return new CPU
            {
                Brand = Brand,
                Model = modelParserResult.Model,
                Benchmark = Benchmark,
                Price = Price,
                Url = Url
            };
        }

        public IComplexComponent SpecificationParser(string specification, OptionCollection options)
        {
            string cores = Regex.Match(specification,
                "Количество ядер</td><td class=\"gr\\d\">(.+)</td></tr>").Groups[1].Value;
            Cores = int.Parse(cores);

            string threads = Regex.Match(specification,
                "Количество потоков</td><td class=\"gr\\d\">(.+)</td></tr>").Groups[1].Value;
            if (threads.Length == 0)
                Threads = int.Parse(cores) * 2;
            else
                Threads = int.Parse(threads);

            string socketTitle = Regex.Match(specification,
                "Разъем</td><td class=\"gr\\d\">(.+)</td></tr>").Groups[1].Value;
            int removeIndex = socketTitle.IndexOf('-');
            if (removeIndex >= 0)
                socketTitle = socketTitle.Remove(removeIndex);
            Socket socket = Server.FindOrAdd(socketTitle, options.Sockets, new Socket());
            Socket = socket.Id;

            string frequency = Regex.Match(specification,
                "Частота, МГц</td><td class=\"gr\\d\">([^ <]+).*</td></tr>").Groups[1].Value;
            Frequency = int.Parse(frequency);
            return this;
        }
    }
}