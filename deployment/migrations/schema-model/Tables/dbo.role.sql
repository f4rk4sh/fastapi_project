CREATE TABLE [dbo].[role]
(
[id] [int] NOT NULL IDENTITY(1, 1),
[name] [varchar] (50) NULL
)
GO
ALTER TABLE [dbo].[role] ADD CONSTRAINT [PK__role__3213E83FE536D4B2] PRIMARY KEY CLUSTERED ([id])
GO
CREATE NONCLUSTERED INDEX [ix_role_id] ON [dbo].[role] ([id])
GO
