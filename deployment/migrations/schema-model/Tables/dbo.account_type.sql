CREATE TABLE [dbo].[account_type]
(
[id] [int] NOT NULL IDENTITY(1, 1),
[name] [varchar] (50) NULL
)
GO

ALTER TABLE [dbo].[account_type] ADD CONSTRAINT [PK__account_type__id] PRIMARY KEY CLUSTERED ([id])
GO

CREATE NONCLUSTERED INDEX [ix_account_type_id] ON [dbo].[account_type] ([id])
GO
