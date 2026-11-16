<#
Ejecuta los programas existentes y muestra dos tablas de la demostracion.
No escribe en resultados/ ni en graficas/ del experimento historico.
#>
param(
    [ValidateSet(1, 20)][int]$Repeticiones = 1,
    [switch]$Graficas,
    [string]$PythonExe,
    [string]$JavacExe,
    [string]$JavaExe
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
$demo = Join-Path $root 'demostracion'
$results = Join-Path $demo 'resultados'
$figures = Join-Path $demo 'graficas'

if (-not $PythonExe) {
    $PythonExe = @(Get-Command python.exe -CommandType Application -ErrorAction Stop)[0].Source
}
if (-not $JavacExe) {
    $adoptium = Join-Path $env:LOCALAPPDATA 'Programs\Eclipse Adoptium'
    if (Test-Path -LiteralPath $adoptium) {
        $candidates = @(Get-ChildItem -LiteralPath $adoptium -Directory |
            Sort-Object Name -Descending |
            ForEach-Object { Join-Path $_.FullName 'bin\javac.exe' } |
            Where-Object { Test-Path -LiteralPath $_ })
        if ($candidates.Count -gt 0) { $JavacExe = $candidates[0] }
    }
    if (-not $JavacExe) {
        $JavacExe = @(Get-Command javac.exe -CommandType Application -ErrorAction Stop)[0].Source
    }
}
if (-not $JavaExe) {
    $JavaExe = Join-Path (Split-Path -Parent $JavacExe) 'java.exe'
}
foreach ($exe in @($PythonExe, $JavacExe, $JavaExe)) {
    if (-not (Test-Path -LiteralPath $exe -PathType Leaf)) {
        throw "Ejecutable no encontrado: $exe"
    }
}

$runner = Join-Path $root 'tests\ejecutar_experimentos.py'
$completed = 0
$expected = 4 * $Repeticiones
$timer = [Diagnostics.Stopwatch]::StartNew()
Write-Host "Iniciando $Repeticiones repeticion(es), hasta $($expected * 2) resultados Python/Java."
& $PythonExe $runner --repeticiones $Repeticiones --resultados $results `
    --python $PythonExe --javac $JavacExe --java $JavaExe 2>&1 |
    ForEach-Object {
        $line = [string]$_
        if ($line -match ' N=\d+ ') {
            $completed++
            if ($completed % 4 -eq 0) {
                $done = [int]($completed / 4)
                Write-Host "Progreso: $done/$Repeticiones repeticiones; $([int]$timer.Elapsed.TotalSeconds) s transcurridos."
            }
        }
        else { Write-Host $line }
    }
if ($LASTEXITCODE -ne 0) { throw 'Fallo la ejecucion; revise el mensaje anterior.' }
Write-Host "Calculo terminado en $([int]$timer.Elapsed.TotalSeconds) s."

$csv = Join-Path $results 'corridas.csv'
$records = @(Import-Csv -LiteralPath $csv -Encoding UTF8)
$sizes = @(1000, 10000, 100000, 1000000)
$pythonRows = @()
$javaRows = @()
foreach ($n in $sizes) {
    $pair = @($records | Where-Object { [int]$_.n -eq $n -and $_.repeticion -eq '1' -and $_.semilla -eq '42' })
    $py = @($pair | Where-Object { $_.lenguaje -eq 'Python' })
    $ja = @($pair | Where-Object { $_.lenguaje -eq 'Java' })
    if ($py.Count -ne 1 -or $ja.Count -ne 1) { throw "Falta una pareja para N=$n" }
    if ($py[0].nc -ne $ja[0].nc -or $py[0].pi_estimado -ne $ja[0].pi_estimado) {
        throw "Diferencia Python/Java para N=$n"
    }
    if ($n -eq 1000 -and ($py[0].nc -ne '773' -or $py[0].pi_estimado -ne '3.092')) {
        throw 'Fallo la referencia N=1000, semilla=42'
    }
    $pythonRows += [pscustomobject]@{
        N = $n
        'Pi estimado' = $py[0].pi_estimado
        'Error absoluto' = $py[0].error_absoluto
        'Tiempo (ms)' = $py[0].tiempo_ms
    }
    $javaRows += [pscustomobject]@{
        N = $n
        'Pi estimado' = $ja[0].pi_estimado
        'Error absoluto' = $ja[0].error_absoluto
        'Tiempo (ms)' = $ja[0].tiempo_ms
    }
}

Write-Host "`nPYTHON - semilla 42"
Write-Host (($pythonRows | Format-Table -AutoSize | Out-String -Width 180).TrimEnd())
Write-Host "`nJAVA - semilla 42"
Write-Host (($javaRows | Format-Table -AutoSize | Out-String -Width 180).TrimEnd())
Write-Host "`nEquivalencia numerica confirmada para los cuatro N (Nc y Pi estimado)."
Write-Host "CSV nuevos: $results"

if ($Graficas) {
    $plotter = Join-Path $root 'tests\graficar_resultados.py'
    $plotOutput = & $PythonExe $plotter --resultados $results --graficas $figures 2>&1
    if ($LASTEXITCODE -ne 0) { throw "Fallo la generacion de graficas: $($plotOutput | Out-String)" }
    Write-Host "Graficas nuevas: $figures"
    if ($Repeticiones -eq 1) {
        Write-Host 'Se generaron 3 graficas; distribucion.png requiere 20 repeticiones.'
    }
    else {
        Write-Host 'Se generaron las 4 graficas, incluida distribucion.png.'
    }
}
