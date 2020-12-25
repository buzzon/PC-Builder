using System.Text.RegularExpressions;

namespace PCBParser
{
    class GPU : IComplexComponent
    {
        public int Brand { get; set; }
        public string Model { get; set; }
        public double Benchmark { get; set; }
        public int Price { get; set; }
        public string Url { get; set; }

        public int Memory { get; set; }

        public dynamic ModelParser(string model)
        {
            model = model.Replace("-6GB", "");
            model = model.Replace("S (Super)", " Super");
            model = model.Replace('-', ' ');

            return new
            {
                Model = model,
                ComparerModel = model.ToLower()
            };
        }

        public bool RepeatComparer(dynamic modelParserResult) =>
            Model == modelParserResult.Model;

        public bool PriceComparer(string componentName, dynamic modelParserResult) =>
            componentName.Contains("видеокарта") &&
            componentName.Contains(modelParserResult.ComparerModel) &&
            (modelParserResult.ComparerModel.Contains("super") ||
            !componentName.Contains("super")) &&
            (modelParserResult.ComparerModel.Contains("ti") ||
            !componentName.Contains("ti"));

        public IComponent Constructor(OptionCollection options, dynamic modelParserResult)
        {
            return new GPU
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
            string memory = Regex.Match(specification, 
                "Объем памяти</td><td class=\"gr\\d\">(.+)</td></tr>").Groups[1].Value;
            if (memory.Length == 0)
                return null;
            int index = memory.IndexOf('/');
            if (index > 0)
                memory = memory.Remove(index);
            Memory = int.Parse(memory);
            return this;
        }
    }
}