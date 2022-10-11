CREATE TABLE [dbo].[status_type]
(
[id] [int] NOT NULL IDENTITY(1, 1),
[name] [varchar] (50) NULL
)
GO

ALTER TABLE [dbo].[status_type] ADD CONSTRAINT [PK__status_type__id] PRIMARY KEY CLUSTERED ([id])
GO

CREATE NONCLUSTERED INDEX [ix_status_type_id] ON [dbo].[status_type] ([id])
GO

CREATE UNIQUE NONCLUSTERED INDEX [ix_status_type_name] ON [dbo].[status_type] ([name])
GO
