IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'db')
BEGIN
  CREATE DATABASE [db];
END;
GO

USE [db];
GO