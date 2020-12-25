using System;
using System.Text.Json.Serialization;

namespace PCBParser
{
    interface IComponent
    {
        int Brand { get; set; }
        string Model { get; set; }
        double Benchmark { get; set; }
        int Price { get; set; }
        string Url { get; set; }
        dynamic ModelParser(string model);
        bool RepeatComparer(dynamic modelParserResult);
        bool PriceComparer(string componentName, dynamic modelParserResult);
        IComponent Constructor(OptionCollection options, dynamic modelParserResult);
    }
}