# Remove build and dist folders
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue build, dist

# Remove all *.egg-info directories in the current folder
Get-ChildItem -Directory -Filter *.egg-info | ForEach-Object {
    Remove-Item -Recurse -Force -ErrorAction SilentlyContinue $_.FullName
}