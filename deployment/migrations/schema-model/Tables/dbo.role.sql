CREATE TABLE [dbo].[role]
(
[id] [int] NOT NULL IDENTITY(1, 1),
[name] [varchar] (50) NULL
)
GO

ALTER TABLE [dbo].[role] ADD CONSTRAINT [PK__role__id] PRIMARY KEY CLUSTERED ([id])
GO

CREATE NONCLUSTERED INDEX [ix_role_id] ON [dbo].[role] ([id])
GO

CREATE UNIQUE NONCLUSTERED INDEX [ix_role_name] ON [dbo].[role] ([name])
GO
