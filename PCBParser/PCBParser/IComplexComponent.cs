namespace PCBParser
{
    interface IComplexComponent : IComponent
    {
        IComplexComponent SpecificationParser(string specification, OptionCollection options);
    }
}