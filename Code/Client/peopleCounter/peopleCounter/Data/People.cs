using Microsoft.AspNetCore.Http.Features;

namespace peopleCounter.Data
{
    public class People : Person
    {
        public People()
        {
            Items = new();
        }

        public List<Person> Items { get; set; }

    }
}