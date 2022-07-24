CREATE DATABASE [db]
GO

USE [db];
GO

CREATE TABLE users (
    Id INT NOT NULL IDENTITY,
    Name TEXT NOT NULL,
    PRIMARY KEY (Id)
);
GO

INSERT INTO [users] (Name)
VALUES
('John Doe'),
('Lora Palmer');
GO