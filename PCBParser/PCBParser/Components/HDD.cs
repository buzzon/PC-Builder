using System.Globalization;
using System.Text.RegularExpressions;

namespace PCBParser
{
    class HDD : IComponent
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
            if (capacity.Length <= 2)
                return null;
            model = model.Remove(capacityIndex);
            int resultCapacity;
            if (capacity.Contains("GB"))
            {
                resultCapacity = int.Parse(capacity.Replace("GB", ""));
                capacity = capacity.Replace("GB", " гб");
            }
            else if (capacity.Contains("TB"))
            {
                resultCapacity = (int)(double.Parse(capacity.Replace("TB", ""), CultureInfo.InvariantCulture) * 1024);
                capacity = capacity.Replace("TB", " тб");
            }
            else
                return null;

            string formfactor = "3.5\"";
            if (model.Contains("2.5\""))
                formfactor = "2.5\"";

            model = model.Replace("2.5\"", "").Trim();

            return new
            {
                Model = model,
                Capacity = resultCapacity,
                Formfactor = formfactor,
                ComparerCapacity = capacity
            };
        }

        public bool RepeatComparer(dynamic modelParserResult) =>
            Model == modelParserResult.Model;

        public bool PriceComparer(string componentName, dynamic modelParserResult) =>
            componentName.Contains("жесткий диск") &&
            componentName.Contains(modelParserResult.Model.ToLower()) &&
            componentName.Contains(modelParserResult.ComparerCapacity);

        public IComponent Constructor(OptionCollection options, dynamic modelParserResult)
        {
            Formfactor formfactor = Server.FindOrAdd(modelParserResult.Formfactor, options.Formfactors, new Formfactor());
            return new HDD
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