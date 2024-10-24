from plagiarism_checker_tf_idf import plagiarism_checker

datos = [
    {
        "codigo_sql": "-- INIT database\nCREATE TABLE Product (\n  ProductID INT AUTO_INCREMENT KEY,\n  Name VARCHAR(100),\n  Description VARCHAR(255)\n);\n\nINSERT INTO Product(Name, Description) VALUES ('Entity Framework Extensions', 'Use <a href=\"https://entityframework-extensions.net/\" target=\"_blank\">Entity Framework Extensions</a> to extend your DbContext with high-performance bulk operations.');\nINSERT INTO Product(Name, Description) VALUES ('Dapper Plus', 'Use <a href=\"https://dapper-plus.net/\" target=\"_blank\">Dapper Plus</a> to extend your IDbConnection with high-performance bulk operations.');\nINSERT INTO Product(Name, Description) VALUES ('C# Eval Expression', 'Use <a href=\"https://eval-expression.net/\" target=\"_blank\">C# Eval Expression</a> to compile and execute C# code at runtime.');\n\n-- QUERY database\nSELECT * FROM Product;\nSELECT * FROM Product WHERE ProductID = 1;",
        "estudiante": {
            "apellidos": "ALBAN CHUQUIPOMA",
            "dni": "18195497",
            "nombres": "MIRIAM JACKELINE"
        },
        "id_codigo": 2,
        "url_codigo": "https://sqlfiddle.com/mysql/online-compiler?&id=ceaf69f5-a283-4f8a-a826-0001e0fd115b"
    },
    {
        "codigo_sql": "-- INIT database\nCREATE TABLE Product (\n  ProductID INT AUTO_INCREMENT KEY,\n  Name VARCHAR(100),\n  Description VARCHAR(255)\n);\n​\nINSERT INTO Product(Name, Description) VALUES ('Entity Framework Extensions', 'Use <a href=\"https://entityframework-extensions.net/\" target=\"_blank\">Entity Framework Extensions</a> to extend your DbContext with high-performance bulk operations.');\nINSERT INTO Product(Name, Description) VALUES ('Dapper Plus', 'Use <a href=\"https://dapper-plus.net/\" target=\"_blank\">Dapper Plus</a> to extend your IDbConnection with high-performance bulk operations.');\nINSERT INTO Product(Name, Description) VALUES ('C# Eval Expression', 'Use <a href=\"https://eval-expression.net/\" target=\"_blank\">C# Eval Expression</a> to compile and execute C# code at runtime.');\n​\n-- QUERY database\nSELECT * FROM Product;\nSELECT * FROM Product WHERE ProductID = 1;\n-- hola",
        "estudiante": {
            "apellidos": "ANDIA DE LA CRUZ",
            "dni": "40434926",
            "nombres": "JAVIER WALTER"
        },
        "id_codigo": 6,
        "url_codigo": "https://sqlfiddle.com/mysql/online-compiler?&id=611a3792-6aa5-43ca-b75d-7f37c62d4fc9"
    },
    {
        "codigo_sql": "-- 1. Crear la base de datos\nCREATE DATABASE farmacia;\nUSE farmacia;\n\n-- 2. Tabla de sucursales\nCREATE TABLE sucursal (\n    id_sucursal INT AUTO_INCREMENT PRIMARY KEY,\n    nombre VARCHAR(100) NOT NULL,\n    direccion VARCHAR(255) NOT NULL,\n    telefono VARCHAR(15),\n    ciudad VARCHAR(100) NOT NULL\n);\n\n-- 3. Tabla de productos (medicamentos y otros)\nCREATE TABLE producto (\n    id_producto INT AUTO_INCREMENT PRIMARY KEY,\n    nombre VARCHAR(100) NOT NULL,\n    descripcion TEXT,\n    precio DECIMAL(10, 2) NOT NULL,\n    stock INT NOT NULL,\n    fecha_vencimiento DATE,\n    id_sucursal INT,\n    FOREIGN KEY (id_sucursal) REFERENCES sucursal(id_sucursal)\n);\n\n-- 4. Tabla de empleados\nCREATE TABLE empleado (\n    id_empleado INT AUTO_INCREMENT PRIMARY KEY,\n    nombre VARCHAR(100) NOT NULL,\n    apellido VARCHAR(100) NOT NULL,\n    cargo VARCHAR(50),\n    salario DECIMAL(10, 2),\n    id_sucursal INT,\n    FOREIGN KEY (id_sucursal) REFERENCES sucursal(id_sucursal)\n);\n\n-- 5. Tabla de clientes\nCREATE TABLE cliente (\n    id_cliente INT AUTO_INCREMENT PRIMARY KEY,\n    nombre VARCHAR(100) NOT NULL,\n    apellido VARCHAR(100) NOT NULL,\n    telefono VARCHAR(15),\n    direccion VARCHAR(255)\n);\n\n-- 6. Tabla de ventas\nCREATE TABLE venta (\n    id_venta INT AUTO_INCREMENT PRIMARY KEY,\n    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\n    total DECIMAL(10, 2) NOT NULL,\n    id_cliente INT,\n    id_empleado INT,\n    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente),\n    FOREIGN KEY (id_empleado) REFERENCES empleado(id_empleado)\n);\n\n-- 7. Tabla de detalle de venta (productos vendidos)\nCREATE TABLE detalle_venta (\n    id_detalle INT AUTO_INCREMENT PRIMARY KEY,\n    id_venta INT,\n    id_producto INT,\n    cantidad INT NOT NULL,\n    subtotal DECIMAL(10, 2) NOT NULL,\n    FOREIGN KEY (id_venta) REFERENCES venta(id_venta),\n    FOREIGN KEY (id_producto) REFERENCES producto(id_producto)\n);",
        "estudiante": {
            "apellidos": "AMANQUI CONDORI",
            "dni": "72664197",
            "nombres": "ASTRID VANESA ELLY"
        },
        "id_codigo": 9,
        "url_codigo": "https://sqlfiddle.com/mysql/online-compiler?id=404da7b2-a2e3-4a29-afb3-9b72d43edb18"
    },
    {
        "codigo_sql": "-- INIT databasef\n  ProductID INT AUTO_INCREMENT KEY,\n  Name VARCHAR(100),sae, Descripwaon) VALUES ('Entity Framework Extensions', 'Use <a href=\"https://entityframework-extensions.net/\" target=\"_blank\">Entity Framework Extensions</a> to extend your DbContext with high-performance bulk operations.');\nINSERT INTO Product(Name, gawgaw)ga VALUES ('Dapper Plus', 'Use <a href=\"https://dapper-plus.net/\" target=\"_blank\">Dapper Plus</a> to extend your IDbConnection with high-performance bulk operations.');\nINSERT INTO Product(Name, Description) VgawgawLUES ('C# Eval Expression', 'Use <a href=\"https://eval-expression.net/\" target=\"_blank\">C# Eval Expression</a> to compile and execute C# code at runtime.');\nfwctID = 1;a",
        "estudiante": {
            "apellidos": "AGIP RUBIO",
            "dni": "27440013",
            "nombres": "RICARDO GERMAN"
        },
        "id_codigo": 13,
        "url_codigo": "https://sqlfiddle.com/mysql/online-compiler?id=0e48b6a6-3566-4409-9fa0-40d034d4bce8"
    }
]
json_result = plagiarism_checker(datos, 0.8)
print(json_result)