$descriptions = Get-Content ".\module_descriptions.txt"
foreach ($line in $descriptions) {
    $parts = $line -split '\|', 2
    $module = $parts[0]
    $desc = $parts[1]
    $schemaPath = ".\modules\$module\schema.md"
    if (Test-Path $schemaPath) {
        # Read all lines from schema
        $content = Get-Content $schemaPath
        # Replace the line starting with description:
        $newContent = $content -replace "^description:.*", "description: $desc"
        # Save back to file
        $newContent | Set-Content $schemaPath
        Write-Host "Updated: $schemaPath"
    } else {
        Write-Host "Schema not found for $module"
    }
}
