using System.Text.RegularExpressions;

namespace PCBParser
{
    class SSD : IComponent
    {
        public int Brand { get; set; }
        public string Model { get; set; }
        public double Benchmark { get; set; }
        public int Price { get; set; }
        public string Url { get; set; }

        public int Formfactor { get; set; }
        public int Capacity { get; set; }

        public dynamic ModelParser(string model)
        {
            Regex bracketRegex = new Regex(@" \(.*\)");
            MatchCollection matches = bracketRegex.Matches(model);
            foreach (Match match in matches)
                model = model.Replace(match.Value, "");

            int capacityIndex = model.LastIndexOf(' ');
            string capacity = model.Substring(capacityIndex + 1);
            model = model.Remove(capacityIndex);
            int resultCapacity;
            if (capacity.Contains("GB"))
                resultCapacity = int.Parse(capacity.Replace("GB", ""));
            else if (capacity.Contains("TB"))
                resultCapacity = int.Parse(capacity.Replace("TB", "")) * 1024;
            else
                return null;

            string formfactor = "2.5\"";
            if (model.Contains("M.2"))
                formfactor = "M.2";

            model = model
                .Replace("M.2", "")
                .Replace("SATA", "")
                .Replace("mSATA", "")
                .Replace("2.5", "")
                .Replace("2.5\"", "")
                .Replace("7mm", "")
                .Replace("NVMe", "")
                .Replace("PCIe", "").Trim();

            if (model.Length == 0)
                return null;

            return new
            {
                Model = model,
                Capacity = resultCapacity,
                Formfactor = formfactor,
                ComparerCapacity = $"{resultCapacity} гб"
            };
        }

        public bool RepeatComparer(dynamic modelParserResult) =>
            Model == modelParserResult.Model;

        public bool PriceComparer(string componentName, dynamic modelParserResult) =>
            (componentName.Contains("ssd-накопитель") ||
            componentName.Contains("ssd m.2 накопитель")) &&
            componentName.Contains(modelParserResult.Model.ToLower()) &&
            componentName.Contains(modelParserResult.ComparerCapacity);

        public IComponent Constructor(OptionCollection options, dynamic modelParserResult)
        {
            Formfactor formfactor = Server.FindOrAdd(modelParserResult.Formfactor, options.Formfactors, new Formfactor());
            return new SSD
            {
                Brand = Brand,
                Model = modelParserResult.Model,
                Benchmark = Benchmark,
                Price = Price,
                Url = Url,
                Formfactor = formfactor.Id,
                Capacity = modelParserResult.Capacity
            };
        }
    }
}