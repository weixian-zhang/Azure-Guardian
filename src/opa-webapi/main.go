package main

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"github.com/open-policy-agent/opa/rego"
	"log"
	"os"
	// "reflect"
)

//https://www.openpolicyagent.org/docs/latest/integration/#integrating-with-the-go-api

func main() {

	input := `{
		"id": "/subscriptions/ee611083-4581-4ba1-8116-a502d4539206/resourceGroups/AzureBackupRG_southeastasia_1/providers/Microsoft.Compute/restorePointCollections/AzureBackup_vm-web_140738144265919",
		"name": "AzureBackup_vm-web_140738144265919",
		"type": "microsoft.compute/restorepointcollections",
		"tenantId": "72f988bf-86f1-41af-91ab-2d7cd011db47",
		"kind": "",
		"location": "southeastasia",
		"resourceGroup": "azurebackuprg_southeastasia_1",
		"subscriptionId": "ee611083-4581-4ba1-8116-a502d4539206",
		"managedBy": "",
		"sku": null,
		"plan": null,
		"properties": {
			"source": {
				"id": "/subscriptions/ee611083-4581-4ba1-8116-a502d4539206/resourceGroups/rgGCCSHOL/providers/Microsoft.Compute/virtualMachines/vm-web"
			}
		},
		"tags": null
	}`

	inputJ := json.NewDecoder(bytes.NewBufferString(input))
	// Numeric values must be represented using json.Number.
	inputJ.UseNumber()

	ctx := context.Background()

	policy := `

		package test

		allow {
			is_compliance = is_tenantId_allowed
		}
		
		is_tenantId_allowed { 
			input.tenantId == "72f988bf-86f1-41af-91ab-2d7cd011db47" 
		}
	`

	ioerr := os.WriteFile("temp.rego", []byte(policy), 0644)
	hasError(ioerr)
	defer os.Remove("temp.rego")

	query, err := rego.New(
		rego.Query("x = data.test"),
		rego.Module("temp.rego", policy),
	).PrepareForEval(ctx)

	hasError(err)

	ctx = context.TODO()
	results, err := query.Eval(ctx, rego.EvalInput(input))

	if err != nil {
		// Handle evaluation error.
		hasError(err)
	} else if len(results) == 0 {
		// Handle undefined result.
	} else if _, ok := results[0].Bindings["x"].(bool); !ok {

		expressions := results[0].Expressions[0]
		jsonExpr, err := json.Marshal(expressions)
		fmt.Println(string(jsonExpr))

		resultMaps := results[0].Bindings["x"]
		rmaps, _ := resultMaps.(map[string]interface{})

		jsonByte, err := json.Marshal(rmaps)

		if !hasError(err) {
			jStr := string(jsonByte)
			fmt.Println(jStr)
		}

		// rv := reflect.ValueOf(results[0].Bindings["x"])

		// if rv.Kind() == reflect.Map {
		// 	for _, key := range rv.MapKeys() {
		// 		strct := rv.MapIndex(key)
		// 		fmt.Println(key.Interface(), strct.Interface())
		// 	}
		// }

		// // Handle unexpected result type.
		// fmt.Println(result)

	} else {
		// Handle result/decision.
		// fmt.Printf("%+v", results) => [{Expressions:[true] Bindings:map[x:true]}]
	}
}

func hasError(err error) bool {
	if err != nil {
		log.Fatalln(err)
		return true
	}
	return false
}
