var express = require("express");
var app = express();
const port = 3000;

app.get("/", function (req, res) {

  console.log("Iniciando descarga...");
  //res.send('Iniciando descarga');

  var spawn = require("child_process").spawn,
    ls = spawn("cmd.exe", ["/c", "prueb.bat"]);

  ls.stdout.on("data", function (data) {
    //console.log('stdout: ' + data);
  });

  ls.stderr.on("data", function (data) {
    //console.log('stderr: ' + data);
  });

  ls.on("exit", function (code) {
    //console.log('child process exited with code ' + code);

    //Listar archivos OSFDocuments
    const path = require("path");
    const fs = require("fs");

    var data = [];

    console.log("Buscando...");
    function scanDirs(directoryPath) {
      try {
        var ls = fs.readdirSync(directoryPath);

        for (let index = 0; index < ls.length; index++) {
          const file = path.join(directoryPath, ls[index]);
          var dataFile = null;
          try {
            dataFile = fs.lstatSync(file);
          } catch (e) {}

          if (dataFile) {
            data.push({
              path: file,
              isDirectory: dataFile.isDirectory(),
              length: dataFile.size,
            });

            if (dataFile.isDirectory()) {
              scanDirs(file);
            }
          }
        }
      } catch (e) {}
    }

    scanDirs("../OSFDocuments");

    console.log(data);

    const jsonString = JSON.stringify(data);

    fs.writeFile("./resultado.json", jsonString, (err) => {
      if (err) {
        //console.log('Error al escribir en el archivo', err)
      } else {
        //console.log('Archivo guardado.')
      }
    });

    //res.send("Descarga terminada");
    const jsonString2 = JSON.stringify("Download Completed");
    res.json(jsonString2);
    console.log("Descarga terminada");
  });
});

var server = app.listen(port, function () {
  var host = server.address().address;
  var port = server.address().port;

  console.log("osf client app listening!", host, port);
});

