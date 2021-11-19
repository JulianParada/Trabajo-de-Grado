const functions = require("firebase-functions");

const express = require("express");
const cors = require("cors");
const app = express();
var nodemailer = require('nodemailer');

var corsOptions = {
  //origin: "http://localhost:8081",
  // origin: "http://localhost:4200",
  origin: "https://gat-gate.firebaseapp.com"
};

app.use(cors(corsOptions));

app.use(express.json());

app.use(express.urlencoded({ extended: true }));

app.get("/", function (req, res) {
  res.send("Got a POST request");
});

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
    connectionTimeout : 90000000
  },
};

const connection = new Connection(config);
var is_connected = false;

// Attempt to connect and execute queries if connection goes through
connection.on("connect", (err) => {
  if (err) {
    console.error(err.message);
  } else {
    //queryDatabase();
    //get_One();
    console.log("Conexion exitosa");
  }
});

connection.connect();

var transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: 'plataformagatgate@gmail.com',
    pass: 'gatgate2021'
  }
});

app.get("/reset_password", (req, res) => {
  var correo = req.query["data"];
  var password =  generatePassword();
  var query = "UPDATE [dbo].[USUARIO] SET PASSWORD = '"+ password+"' WHERE EMAIL = '"+ correo+"' ";
  console.log(query);
  
  const request = new Request(query, (err, rowCount) => {
      if (err) {
        console.error(err.message);
        res.send(err.message);
      } else {
        console.log(`${rowCount} row(s) returned`);
        res.send("Insertada correctamente " + `${rowCount}`+ " registro(s  ) ");
        if (rowCount > 0) {
          var mailOptions = {
            from: 'plataformagatgate@gmail.com',
            to: correo,
            subject: 'Cambio Contraseña Cuenta GAT Gate',
            html:"<h3>Atencion</h3><br><h3>Se ha cambiado tu contraseña </h3><br><p> Tu nueva contraseña es :"+password+ "</p>"
          };
  
          transporter.sendMail(mailOptions, function(error, info){
            if (error) {
              console.log(error);
            } else {
              console.log('Email sent: ' + info.response);
            }
          });
        }
      }
    });
    connection.execSql(request);
  });

//Comando cuando se pida un path.
app.get("/getAll_usuarios", (req, res) => {
  console.log("Reading rows from the Table...");
  const request = new Request(
    "SELECT * FROM [dbo].[USUARIO]",
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

app.get("/getOne_usuario", (req, res) => {
  var input = req.query["data"];
  var query = "SELECT * FROM [dbo].[USUARIO] WHERE EMAIL ='"+input+ "'";
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
    //console.log(columns);
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

app.get("/add_One_usuario", (req, res) => {
  var input = req.query["data"];
  var array = input.split("|");
  var correo;
  var password;
  var query = "INSERT INTO [dbo].[USUARIO] VALUES (";

  for (var i = 0; i < array.length; i++) {
    if (i > 0) {
      query = query + ",";
    }
    if (array[i].substring(0, 3) == "NUL") {
      query = query + "NULL";
    }
    if (array[i].substring(0, 4) == "PASS") {
      //AGREGAR AQUI LA CONTRA JEJE
      password =  generatePassword()
      query = query +"'" + password +"'";
    }
    if (array[i].substring(0, 4) == "MAIL") {
      //AGREGAR AQUI LA CONTRA JEJE
      query = query + "'" + array[i].substring(4, array[i].length) + "'";
      correo = array[i].substring(4, array[i].length)
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
  console.log(query);

  const request = new Request(query, (err, rowCount) => {
    if (err) {
      console.error(err.message);
      res.send(err.message);
    } else {
      console.log(`${rowCount} row(s) returned`);
      res.send("Insertada correctamente " + `${rowCount}` + " registro(s  ) ");
      if (rowCount > 0) {
        var mailOptions = {
          from: 'plataformagatgate@gmail.com',
          to: correo,
          subject: 'Credenciales Cuenta GAT Gate',
          text: 'Felicitaciones por la creación de tu usuario GAT Gate,  puedes ingresar con el correo ' +  correo
          + ' tu contraseña para acceder es :'+ password + ''
        };

        transporter.sendMail(mailOptions, function(error, info){
          if (error) {
            console.log(error);
          } else {
            console.log('Email sent: ' + info.response);
          }
        });
      }
    }
  });
  connection.execSql(request);
});

app.get("/update_One_usuario", (req, res) => {
  var input = req.query["data"];
  var array = input.split("|");

  var query = "UPDATE [dbo].[USUARIO] SET ";

  for (var i = 1; i < array.length; i++) {
    //console.log(i);
    //console.log(array.length);
    //http://localhost:8080/update_Actividad?data=actividades|9|STRnumero=A99|STRdescripcion=Contrar%20investigadoressoscios|STRobjetivo_pofi=Acrecion|NULL=fecha|STRtipo=UDEA|FLTporcentaje_Avance=0.9
    if (i > 1) {
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
  query = query + "WHERE EMAIL = '" + array[0] + "'";
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

function generatePassword() {
  var length = 8,
      charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
      retVal = "";
  for (var i = 0, n = charset.length; i < length; ++i) {
      retVal += charset.charAt(Math.floor(Math.random() * n));
  }
  return retVal;
}


//INTERVAL END 
setInterval(function () {
  // console.log(connection.state)
     connection.on("end", (err) => {
     if (err) {
       console.error(err.message);
     } else {
       //queryDatabase();
       //get_One();
       console.log("Conexion Cerrada");
     }
   });
   if(is_connected){
     console.log("desconectar")
     connection.close();
     is_connected = false;
   }
 }, 86400000);  
 
 //INTERVAL BEGIN
 setInterval(function () {
  // console.log(connection.state)
     connection.on("connect", (err) => {
     if (err) {
       console.error(err.message);
     } else {
       //queryDatabase();
       //get_One();
       console.log("Conexion exitosa");
     }
   });
   if(!is_connected){
     connection = new Connection(config)
     console.log("conectar")
     connection.connect();
     is_connected = true;
   }
 }, 86450000);  //35000
 

app.get("/Begin_Connection", (req, res) => {

    connection.on("connect", (err) => {
      if (err) {
        console.error(err.message);
      } else {
        //queryDatabase();
        //get_One();
        res.send("Conexion exitosa");
        console.log("Conexion exitosa");
      }
    });
    if(!is_connected){
        connection.connect();
        is_connected = true;
      }
});
  
app.get("/End_Connection", (req, res) => {
  
    connection.on("end", (err) => {
      if (err) {
        console.error(err.message);
      } else {
        //queryDatabase();
        //get_One();
        res.send("Conexion Cerrada");
        console.log("Conexion Cerrada");
      }
    });
    if(is_connected){
        connection.close();
        is_connected = false;
      }
});

exports.app = functions.https.onRequest(app);