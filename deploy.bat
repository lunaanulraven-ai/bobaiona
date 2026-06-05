@echo off
echo Atualizando VERSION no sw.js...
node -e "const fs=require('fs');const s=fs.readFileSync('sw.js','utf8');fs.writeFileSync('sw.js',s.replace(/VERSION = '[^']*'/,\"VERSION = '\" + new Date().toISOString() + \"'\"));"
if errorlevel 1 ( echo Erro ao atualizar sw.js & exit /b 1 )

for /f "tokens=*" %%i in ('node -e "process.stdout.write(new Date().toISOString())"') do set TS=%%i

echo Commitando...
git add -A
git commit -m "deploy: %TS%"
if errorlevel 1 ( echo Nada pra commitar ou erro no commit & exit /b 1 )

echo Fazendo push...
git push
if errorlevel 1 ( echo Erro no push & exit /b 1 )

echo.
echo Deploy concluido! VERSION = %TS%
