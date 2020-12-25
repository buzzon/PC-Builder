using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Text.Json;

namespace PCBParser
{
    class Server
    {
        const string api_url = "http://188.226.96.115:8000/api/core/";
        static string token = "";

        public static bool LogIn(string username, string password)
        {
            WebClient webClient = new WebClient();
            webClient.Headers[HttpRequestHeader.ContentType] = "application/json";
            string response;
            try
            {
                response = webClient.UploadString($"{api_url}getToken/",
                    $"{{\"username\": \"{username}\", \"password\": \"{password}\"}}");
            }
            catch
            {
                return false;
            }
            int begin = response.IndexOf(":\"") + 2;
            int end = response.IndexOf("\"}");
            token = "Token " + response[begin..end];
            return true;
        }

        static string Serialize<T>(T component)
        {
            JsonSerializerOptions jsonSerializerOptions = new JsonSerializerOptions();
            jsonSerializerOptions.PropertyNamingPolicy = JsonNamingPolicy.CamelCase;
            return JsonSerializer.Serialize(component, jsonSerializerOptions);
        }

        static T Deserialize<T>(string json)
        {
            JsonSerializerOptions jsonSerializerOptions = new JsonSerializerOptions();
            jsonSerializerOptions.PropertyNamingPolicy = JsonNamingPolicy.CamelCase;
            return JsonSerializer.Deserialize<T>(json, jsonSerializerOptions);
        }

        public static List<T> DownloadInfo<T>()
        {
            WebClient webClient = new WebClient();
            webClient.Headers[HttpRequestHeader.Authorization] = token;
            string json = webClient.DownloadString($"{api_url}{typeof(T).Name}/");
            List<T> result = Deserialize<List<T>>(json);
            return result;
        }

        public static T UploadInfo<T>(T component)
        {
            WebClient webClient = new WebClient();
            webClient.Headers[HttpRequestHeader.Authorization] = token;
            webClient.Headers[HttpRequestHeader.ContentType] = "application/json";
            string json = Serialize(component);
            try
            {
                string response = webClient.UploadString($"{api_url}{component.GetType().Name}/", json);
                return Deserialize<T>(response);
            }
            catch (WebException e)
            {
                Console.WriteLine(e.Message);
                using Stream s = e.Response.GetResponseStream();
                using StreamReader sr = new StreamReader(s);
                Console.WriteLine(sr.ReadToEnd());
                return component;
            }
        }

        public static T FindOrAdd<T>(string title, List<T> components, T plug) where T : Option
        {
            T component = components.Find(b => b.Title == title);
            if (component == null)
            {
                plug.Title = title;
                component = UploadInfo(plug);
                components.Add(component);
            }
            return component;
        }
    }
}