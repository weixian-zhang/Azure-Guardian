

		package test

		allow {
			is_compliance = is_tenantId_allowed
		}
		
		is_tenantId_allowed { 
			input.tenantId == "72f988bf-86f1-41af-91ab-2d7cd011db47" 
		}
	