package dataapi.authz

rule[{"action": {"name": "Policies", "columns": "NA", "copyrules" : `[{"action": {"name":"Allow",
        "columns":"\"\"",
        "runtime_eval":["input.request.role == \"foreman\"",
                "input.request.operation == \"READ\""
            ],
            "partial_eval":{}},
        "policy":"Full priviledges for boss"
    },
    {"action": {"name":"RedactColumn",
        "columns":"columns",
        "runtime_eval":["input.request.role == \"worker\"",
                "asset := assets[input.request.asset.namespace][input.request.asset.name]",
                "columns := [c | asset.spec.assetMetadata.componentsMetadata[i].tags[_] == \"PII\"; c = i]"
            ],
            "partial_eval":{}},
        "policy":"Filtering PII columns for workers"
    },
    {"action": {"name":"BlockURL",
        "columns":"\"\"",
        "runtime_eval":["input.request.role == \"worker\"",
                "asset := assets[input.request.asset.namespace][input.request.asset.name]",
                "asset.spec.assetMetadata.tags[_] == \"control\""
            ],
            "partial_eval":{}},
        "policy":"Block controlling robots for Worker"
    },
    {"action": {"name":"BlockURL",
        "columns":"\"\"",
        "runtime_eval":["input.request.role == \"hr\"",
                "asset := assets[input.request.asset.namespace][input.request.asset.name]",
                "asset.spec.assetMetadata.tags[_] == \"control\""
            ],
            "partial_eval":{}},
        "policy":"Block controlling robots for HR"
    },
    {"action": {"name":"BlockURL",
        "columns":"\"\"",
        "runtime_eval":["input.request.role == \"hr\"",
                        "asset := assets[input.request.asset.namespace][input.request.asset.name]",
                        "asset.spec.assetMetadata.tags[_] == \"data\""
                    ],
                    "partial_eval":{}},
                "policy":"Block getting robot and manufacturing data for HR"
    },
    {"action": {"name":"Allow",
            "columns":"\"\"",
            "runtime_eval":["input.request.role == \"hr\"",
                            "asset := assets[input.request.asset.namespace][input.request.asset.name]",
                            "asset.spec.assetMetadata.tags[_] == \"personnel\""
                        ],
                        "partial_eval":{}},
                    "policy":"Allow getting personnel data for HR"
    }
    ]`}, "policy" : "runtime"}] {
1 == 1
}

