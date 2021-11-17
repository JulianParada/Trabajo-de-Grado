const cors = require("cors");
//var Request = require('request');
const { Connection, Request } = require("tedious");
//const { get } = require("request");

// Esta funcion solo recibe el nombre de la tabla.
// Maybe cambiar nombre de la funcion a get_All_Entidad
function get_All_Actividad(connection, table_name) {
  console.log("Reading rows from the Table...");
  const request = new Request(
    "SELECT * FROM [dbo].[" + table_name + "]",
    (err, rowCount) => {
      if (err) {
        console.error(err.message);
      } else {
        console.log(`${rowCount} row(s) returned`);
      }
    }
  );

  request.on("row", (columns) => {
    columns.forEach((column) => {
      console.log("%s\t%s", column.metadata.colName, column.value);
    });
    console.log("--------------------------");
  });

  connection.execSql(request);
}

// Esta funcion recibe un vector de Strings que tienen la siguiente taxonomia:
// table_name,attribute_1,attibute_2,attibute_3.
// Es importante tener los campos, si es necesario colocar NULL, deberia venir de manera explicita, asi:
// actividades|INT4|STRA4|STRContratar investigadores|STRAcreditacion|DATNULL|STRPUJ|FLT0.7
function get_one_Actividad(connection, input) {
  //connection.connect();
  console.log("Reading rows from the Tableeeeeeeeeee...");
  //console.log(input);
  var array = input.split("|");
  //console.log(array[0]);
  //console.log(array[1]);
  const request = new Request(
    "SELECT * FROM [dbo].[" + array[0] + "] WHERE numero ='" + array[1] + "'",
    (err, rowCount) => {
      if (err) {
        console.error(err.message);
      } else {
        console.log(`${rowCount} row(s) returned`);
      }
    }
  );
  request.on("end", (columns) => {
    //. on row  end????
    //console.log("encontre");
    var resultado = "";
    columns.forEach((column) => {
      //console.log("%s\t%s", column.metadata.colName, column.value);
      resultado = resultado + "%s\t%s" + column.metadata.colName + column.value;
    });
    console.log("--------------------------");
      request.json( resultado);
  });

  connection.execSql(request);
  //return "dd"
}

function add_one_Actividad(connection, input) {
  //connection.connect();
  console.log("Creating query");
  //console.log(input);
  var array = input.split("|");
  //console.log(array[2].substring(0, 3));
  //console.log(array[2].substring(3, array[2].length));
  //INSERT INTO [dbo].[actividades] VALUES (A5','Montar una BD', 'Acreditaion','2021-01-01',NULL,1.5)
  var query = "INSERT INTO [dbo].[" + array[0] + "] VALUES (";

  for (var i = 1; i < array.length; i++) {
    console.log(i);
    console.log(array.length);
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
    } else {
      console.log(`${rowCount} row(s) returned`);
    }
  });
  request.on("row", (columns) => {
    //. on row  end????
    console.log("encontre");
    var resultado = "";
    columns.forEach((column) => {
      console.log("%s\t%s", column.metadata.colName, column.value);
      resultado = resultado + "%s\t%s" + column.metadata.colName + column.value;
    });
    console.log("--------------------------");
    //  return "88";
  });

  connection.execSql(request);
  //return "dd"
}
module.exports = { get_All_Actividad, get_one_Actividad, add_one_Actividad };

function sql_injection(input) {
  var norm = input.toLowerCase();
  if (
    norm.includes("--") ||
    norm.includes("//") ||
    norm.includes("/*") ||
    norm.includes("--") ||
    norm.includes(";")  ||
    norm.includes("drop")||
    norm.includes("or") ||
    norm.includes("and")
  ) {
    return false;
  } else {
    return true;
  }
}
/*
function queryDatabase() {
  console.log("Reading rows from the Table...");
  const request = new Request(
    `SELECT TOP (1000) * FROM [dbo].[ingredients]`,
    (err, rowCount) => {
      if (err) {
        console.error(err.message);
      } else {
        console.log(`${rowCount} row(s) returned`);
      }
    }
  );

  request.on("row", columns => {
    columns.forEach(column => {
      console.log("%s\t%s", column.metadata.colName, column.value);
    });
    console.log ('--------------------------');
  });

  connection.execSql(request);
}

  */
