﻿// Copyright (c) Microsoft. All rights reserved.

using System.Collections.Generic;
using System.Linq;

namespace Orchestrator.Model;

public class AskResult
{
    public string Value { get; set; } = string.Empty;

    public IEnumerable<AskInput>? State { get; set; } = Enumerable.Empty<AskInput>();
}
