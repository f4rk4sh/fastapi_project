CREATE TABLE [dbo].[bank]
(
[id] [int] NOT NULL IDENTITY(1, 1),
[name] [varchar] (50) NULL,
[edrpou] [varchar] (50) NULL,
[mfo] [varchar] (50) NULL,
[iban] [varchar] (50) NULL,
[card] [varchar] (50) NULL,
[account_type_id] [int] NULL
)
GO

ALTER TABLE [dbo].[bank] ADD CONSTRAINT [PK__bank__id] PRIMARY KEY CLUSTERED ([id])
GO

CREATE NONCLUSTERED INDEX [ix_bank_id] ON [dbo].[bank] ([id])
GO

ALTER TABLE [dbo].[bank] ADD CONSTRAINT [FK__bank__account_type__id] FOREIGN KEY ([account_type_id]) REFERENCES [dbo].[account_type] ([id]) ON DELETE CASCADE
GO
