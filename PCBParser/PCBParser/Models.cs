using System.Collections.Generic;

namespace PCBParser
{
    class ComponentPrice
    {
        public string ComponentName;
        public string LowerComponentName;
        public int Price;
    }

    class Specification
    {
        public string Name;
        public string Url;
    }

    abstract class Option
    {
        public int Id { get; set; }
        public string Title { get; set; }
    }

    class Brand : Option { }
    class Socket : Option { }
    class MemoryType : Option { }
    class Formfactor : Option { }
    class Chipset : Option { }

    class OptionCollection
    {
        public List<Brand> Brands;
        public List<Socket> Sockets;
        public List<MemoryType> MemoryTypes;
        public List<Formfactor> Formfactors;
        public List<Chipset> Chipsets;
    }
}