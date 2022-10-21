CREATE TABLE [dbo].[bank]
(
[id] [int] NOT NULL IDENTITY(1, 1),
[name] [varchar] (50) NULL,
[mfo] [varchar] (50) NULL,
[is_active] [BIT] NULL DEFAULT 0,
[creation_date] [datetime] NULL,
[deactivation_date] [datetime] NULL
)
GO

ALTER TABLE [dbo].[bank] ADD CONSTRAINT [PK__bank__id] PRIMARY KEY CLUSTERED ([id])
GO

CREATE NONCLUSTERED INDEX [ix_bank_id] ON [dbo].[bank] ([id])
GO
