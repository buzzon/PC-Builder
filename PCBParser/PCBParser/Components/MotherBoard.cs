using System;
using System.Collections.Generic;
using System.Text;

namespace PCBParser
{
    class MotherBoard
    {
        public int Brand { get; set; }
        public string Model { get; set; }
        public int Price { get; set; }
        public string Url { get; set; }

        public int Formfactor { get; set; }
        public int Chipset { get; set; }
        public int Socket { get; set; }
        public int Year { get; set; }
    }
}
