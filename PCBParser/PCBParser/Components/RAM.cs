namespace PCBParser
{
    class RAM : IComponent
    {
        public int Brand { get; set; }
        public string Model { get; set; }
        public double Benchmark { get; set; }
        public int Price { get; set; }
        public string Url { get; set; }

        public int Count { get; set; }
        public int Capacity { get; set; }
        public int Frequency { get; set; }
        public int Type { get; set; }

        public dynamic ModelParser(string model)
        {
            string[] fullInfo = model.Split(' ');
            if (fullInfo.Length == 5)
                model = fullInfo[0];
            else if (fullInfo.Length == 6)
            {
                model = $"{fullInfo[0]} {fullInfo[1]}";
                fullInfo = fullInfo[1..];
            }
            else
                return null;
            string type = fullInfo[1];
            int frequency = int.Parse(fullInfo[2]);
            string capacity = fullInfo[4];

            string[] countCapacity = capacity.Split('x');
            int count = int.Parse(countCapacity[0]);
            int resultCapacity = count * int.Parse(countCapacity[1].Replace("GB", ""));

            return new
            {
                Model = model,
                Count = count,
                Capacity = resultCapacity,
                Frequency = frequency,
                Type = type,
                ComparerCapacity = $"{resultCapacity} гб"
            };
        }

        public bool RepeatComparer(dynamic modelParserResult) =>
            Model == modelParserResult.Model &&
            Frequency == modelParserResult.Frequency &&
            Count == modelParserResult.Count &&
            Capacity == modelParserResult.Capacity;

        public bool PriceComparer(string componentName, dynamic modelParserResult) =>
            componentName.Contains("оперативная память") &&
            componentName.Contains(modelParserResult.Model.ToLower()) &&
            componentName.Contains(modelParserResult.ComparerCapacity);

        public IComponent Constructor(OptionCollection options, dynamic modelParserResult)
        {
            MemoryType memoryType = Server.FindOrAdd(modelParserResult.Type, options.MemoryTypes, new MemoryType());
            return new RAM
            {
                Brand = Brand,
                Model = modelParserResult.Model,
                Benchmark = Benchmark,
                Price = Price,
                Url = Url,
                Count = modelParserResult.Count,
                Capacity = modelParserResult.Capacity,
                Frequency = modelParserResult.Frequency,
                Type = memoryType.Id,
            };
        }
    }
}