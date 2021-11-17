//IMPORTS NECESARIOS : Express y Cors
const express = require("express");
const cors = require("cors");
//const ftd = require("./fetcher.js");
const app = express();

//CONFIGURACION DEL SERVER EXPRESS
var corsOptions = {
  origin: "http://localhost:8081",
};

app.use(cors(corsOptions));

// parse requests of content-type - application/json
app.use(express.json());

// parse requests of content-type - application/x-www-form-urlencoded
app.use(express.urlencoded({ extended: true }));

// simple route
app.get("/", function (req, res) {
  res.send("Got a POST request");
});
// set port, listen for requests
/*const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}.`);
});
*/
app.listen(8081, (req, res) => {
  console.log("running on 8081");
});

//CONFIGURACION CONEXION A LA BD
const { Connection, Request } = require("tedious");
const { get } = require("request");
const { query } = require("express");
// Create connection to database
const config = {
  authentication: {
    options: {
      userName: "admin-gat", // update me
      password: "tesos2021*", // update me
    },
    type: "default",
  },
  server: "testing-serve.database.windows.net", // update me
  options: {
    database: "TESTING", //update me
    encrypt: true,
  },
};

const connection = new Connection(config);

//Comando cuando se pida un path.
app.get("/getAll", (req, res) => {
  var input = req.query["data"];
  console.log("Reading rows from the Table...");
  const request = new Request(
    "SELECT * FROM [dbo].[" + input + "]",
    (err, rowCount) => {
      if (err) {
        console.error(err.message);
      } else {
        console.log(`${rowCount} row(s) returned`);

        resultado = resultado.substring(0, resultado.length - 2);
        resultado = resultado + "]";

        if (rowCount > 0) {
          res.json(resultado);
        } else {
          res.json("[]");
        }
      }
    }
  );
  var resultado = "[";
  request.on("row", (columns) => {
    for (var i = 0; i < columns.length; i++) {
      if (i == 0) {
        resultado = resultado + "{";
      }

      resultado =
      resultado + '"' +columns[i].metadata.colName + '":"' + columns[i].value +'"';

      if (i < columns.length - 1) {
        resultado = resultado + ", ";
      }
      if (i == columns.length - 1) {
        resultado = resultado + "} , ";
      }
      //console.log("--------------------------");
    }
    console.log("--------------------------");
  });
  // res.send(resultado);
  connection.execSql(request);
});

app.get("/getMaxID", (req, res) => {
  var input = req.query["data"];
  console.log("Reading rows from the Table...");
  const request = new Request(
    "SELECT MAX(ID) AS ID FROM [dbo].[" + input + "]",
    (err, rowCount) => {
      if (err) {
        console.error(err.message);
      } else {
        console.log(`${rowCount} row(s) returned`);

        resultado = resultado.substring(0, resultado.length - 2);
        resultado = resultado + "]";

        if (rowCount > 0) {
          res.json(resultado);
        } else {
          res.json("[]");
        }
      }
    }
  );
  var resultado = "[";
  request.on("row", (columns) => {
    for (var i = 0; i < columns.length; i++) {
      if (i == 0) {
        resultado = resultado + "{";
      }

      resultado =
      resultado + '"' +columns[i].metadata.colName + '":"' + columns[i].value +'"';

      if (i < columns.length - 1) {
        resultado = resultado + ", ";
      }
      if (i == columns.length - 1) {
        resultado = resultado + "} , ";
      }
      //console.log("--------------------------");
    }
    console.log("--------------------------");
  });
  // res.send(resultado);
  connection.execSql(request);
});

app.get("/getOne", (req, res) => {
  var input = req.query["data"]; // req.params.nea;
  console.log("Reading rows from the Tableeeeeeeeeee...");
  //console.log(input);
  var array = input.split("|");
  //console.log(array[0]);
  //console.log(array[1]);
  var query;
  if (
    array[2].substring(0, 3) == "INT" ||
    array[2].substring(0, 3) == "FLT" ||
    array[2].substring(0, 3) == "BLN"
  ) {
    query = "SELECT * FROM [dbo].[" + array[0] + "] WHERE "+ array[1] + " ='" + array[2].substring(3, array[2].length) + "'";
  }
  if (
    array[2].substring(0, 3) == "STR" ||
    array[2].substring(0, 3) == "DAT" ||
    array[2].substring(0, 3) == "TSP"
  ) {
    query = "SELECT * FROM [dbo].[" + array[0] + "] WHERE "+ array[1] + " ='" + array[2].substring(3, array[2].length) + "'";
    //"SELECT * FROM [dbo].[" + array[0] + "] WHERE "+ array[1] + " ='" + array[1] + "'"
  }
  console.log(query);
  const request = new Request(query,
    (err, rowCount) => {
      if (err) {
        console.error(err.message);
      } else {
        console.log(`${rowCount} row(s) returned`);

        if (rowCount > 0) {
          res.json(resultado);
        } else {
          res.json("[]");
        }
      }
    }
  );
  var resultado = "[";
  request.on("row", (columns) => {
    //. on row  end????
    console.log(columns);
    for (var i = 0; i < columns.length; i++) {
      if (i == 0) {
        resultado = resultado + "{";
      }
      resultado =
      resultado + '"' +columns[i].metadata.colName + '":"' + columns[i].value +'"';

      if (i < columns.length - 1) {
        resultado = resultado + ", ";
      }
      console.log("--------------------------");
    }
    resultado = resultado + "}]";
  });

  connection.execSql(request);
  //return "dd"
});

app.get("/add_One", (req, res) => {
  var input = req.query["data"];
  var array = input.split("|");
  var query = "INSERT INTO [dbo].[" + array[0] + "] VALUES (";

  for (var i = 1; i < array.length; i++) {
    if (i > 1) {
      query = query + ",";
    }
    if (array[i].substring(0, 3) == "NUL") {
      query = query + "NULL";
    }
    if (
      array[i].substring(0, 3) == "INT" ||
      array[i].substring(0, 3) == "FLT" ||
      array[i].substring(0, 3) == "BLN"
    ) {
      query = query + "" + array[i].substring(3, array[i].length) + "";
    }
    if (
      array[i].substring(0, 3) == "STR" ||
      array[i].substring(0, 3) == "DAT" ||
      array[i].substring(0, 3) == "TSP"
    ) {
      query = query + "'" + array[i].substring(3, array[i].length) + "'";
    }
  }
  query = query + ")";
  //console.log(query);

  const request = new Request(query, (err, rowCount) => {
    if (err) {
      console.error(err.message);
      res.send(err.message);
    } else {
      console.log(`${rowCount} row(s) returned`);
      res.send("Insertada correctamente " + `${rowCount}` + " registro(s  ) ");
    }
  });
  
  connection.execSql(request);
});

app.get("/update_One", (req, res) => {
  var input = req.query["data"];
  var array = input.split("|");

  var query = "UPDATE [dbo].[" + array[0] + "] SET ";

  for (var i = 2; i < array.length; i++) {
    //console.log(i);
    //console.log(array.length);
    //http://localhost:8080/update_Actividad?data=actividades|9|STRnumero=A99|STRdescripcion=Contrar%20investigadoressoscios|STRobjetivo_pofi=Acrecion|NULL=fecha|STRtipo=UDEA|FLTporcentaje_Avance=0.9
    if (i > 2) {
      query = query + ", ";
    }
    if (array[i].substring(0, 3) == "NUL") {
      aux_column = array[i].split("=");
      query = query + aux_column[1]+" = NULL";
    }
    if (
      array[i].substring(0, 3) == "INT" ||
      array[i].substring(0, 3) == "FLT" ||
      array[i].substring(0, 3) == "BLN"
    ) {
      aux_column = array[i].split("=");
      query = query + aux_column[0].substring(3, aux_column[0].length)  + "= " + aux_column[1]+ " ";
    }
    if (
      array[i].substring(0, 3) == "STR" ||
      array[i].substring(0, 3) == "DAT" ||
      array[i].substring(0, 3) == "TSP"
    ) {
      aux_column = array[i].split("=");
      query = query + aux_column[0].substring(3, aux_column[0].length)  + "= '" + aux_column[1]+ "'";
    }
  }
  query = query + "WHERE ID =" + array[1] + "";
  console.log(query);

  const request = new Request(query, (err, rowCount) => {
    if (err) {
      console.error(err.message);
    } else {
      console.log(`${rowCount} row(s) returned`);

      console.log(`${rowCount} row(s) returned`);
      res.send("Insertada correctamente " + `${rowCount}` + " registro(s  ) ");
    }
  });
  // res.send(resultado);
  connection.execSql(request);
});

app.get("/Clean_Table", (req, res) => {
  var input = req.query["data"];
  var query = "DELETE FROM [dbo].[" + input+ "]"; 

  console.log(query);

  const request = new Request(query, (err, rowCount) => {
    if (err) {
      console.error(err.message);
      res.send(err.message);
    } else {
      //console.log(`${rowCount} row(s) returned`);
      res.send("Limpiada correctamente ");
    }
  });
  
  connection.execSql(request);
});

app.get("/getAll_Specs", (req, res) => {
  var input = req.query["data"];

  var array = input.split("|");

  var query = "SELECT "
  for(var j=1; j < array.length ; j++){
    
    query = query + array[j]

    if(j <  array.length ){
      query = query +" ,"
    }
  }
  query = query.substring(0, query.length -1)
  query = query + " from [dbo].[" + array[0] + "]"

  console.log(query)
  console.log("Reading rows from the Table...");
  const request = new Request(query,
    (err, rowCount) => {
      if (err) {
        console.error(err.message);
      } else {
        console.log(`${rowCount} row(s) returned`);

        resultado = resultado.substring(0, resultado.length - 2);
        resultado = resultado + "]";

        if (rowCount > 0) {
          res.json(resultado);
        } else {
          res.json("[]");
        }
      }
    }
  );
  var resultado = "[";
  request.on("row", (columns) => {
    for (var i = 0; i < columns.length; i++) {
      if (i == 0) {
        resultado = resultado + "{";
      }

      resultado =
      resultado + '"' +columns[i].metadata.colName + '":"' + columns[i].value +'"';

      if (i < columns.length - 1) {
        resultado = resultado + ", ";
      }
      if (i == columns.length - 1) {
        resultado = resultado + "} , ";
      }
      //console.log("--------------------------");
    }
    console.log("--------------------------");
  });
  // res.send(resultado);
  connection.execSql(request);
});

app.get("/Begin_Connection", (req, res) => {

  connection.on("connect", (err) => {
    if (err) {
      console.error(err.message);
    } else {
      //queryDatabase();
      //get_One();
      console.log("Conexion exitosa");
      const jsonString2 = JSON.stringify("Conexion exitosa");
      res.json(jsonString2);
    }
  });
  connection.connect();
});

app.get("/End_Connection", (req, res) => {

  connection.on("end", (err) => {
    if (err) {
      console.error(err.message);
    } else {
      //queryDatabase();
      //get_One();
      console.log("Conexion Cerrada");
      const jsonString2 = JSON.stringify("Conexion Cerrada");
      res.json(jsonString2);
    }
  });
  connection.close();
});
