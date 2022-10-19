IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = "db")
BEGIN
  CREATE DATABASE [db];
  CREATE DATABASE [testdb];
END;
GO

USE [db];
GO