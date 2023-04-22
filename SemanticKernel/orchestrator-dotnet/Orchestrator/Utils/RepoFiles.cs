// Copyright (c) Microsoft. All rights reserved.

using System.IO;
using System.Reflection;

namespace Orchestrator.Utils;

internal static class RepoFiles
{
    /// <summary>
    /// Scan the local folders from the repo, looking for "orchestrator-dotnet/Orchestrator.SemanticSkills" folder.
    /// </summary>
    /// <returns>The full path to orchestrator-dotnet/Orchestrator.SemanticSkills</returns>
    internal static string SemanticSkillsPath()
    {
        const string PARENT = "orchestrator-dotnet";
        const string FOLDER = "Orchestrator.SemanticSkills";

        bool SearchPath(string pathToFind, out string result, int maxAttempts = 10)
        {
            var currDir = Path.GetFullPath(Assembly.GetExecutingAssembly().Location);
            bool found;
            do
            {
                result = Path.Join(currDir, pathToFind);
                found = Directory.Exists(result);
                currDir = Path.GetFullPath(Path.Combine(currDir, ".."));
            } while (maxAttempts-- > 0 && !found);

            return found;
        }

        if (!SearchPath(PARENT + Path.DirectorySeparatorChar + FOLDER, out string path)
            && !SearchPath(FOLDER, out path))
        {
            throw new YourAppException("Skills directory not found. The app needs the skills from the repo to work.");
        }

        return path;
    }
}
