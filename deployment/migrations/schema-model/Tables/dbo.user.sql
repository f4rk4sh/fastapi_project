CREATE TABLE [dbo].[user]
(
[id] [int] NOT NULL IDENTITY(1, 1),
[email] [varchar] (50) NULL,
[password] [varchar] (100) NULL,
[phone] [varchar] (50) NULL,
[creation_date] [datetime] NULL,
[activation_date] [datetime] NULL,
[role_id] [int] NULL,
[status_type_id] [int] NULL
)
GO
ALTER TABLE [dbo].[user] ADD CONSTRAINT [PK__user__id] PRIMARY KEY CLUSTERED ([id])
GO
CREATE UNIQUE NONCLUSTERED INDEX [ix_user_email] ON [dbo].[user] ([email])
GO
CREATE NONCLUSTERED INDEX [ix_user_id] ON [dbo].[user] ([id])
GO
ALTER TABLE [dbo].[user] ADD CONSTRAINT [FK__user__role__id] FOREIGN KEY ([role_id]) REFERENCES [dbo].[role] ([id])
GO
ALTER TABLE [dbo].[user] ADD CONSTRAINT [FK__user__status_type__id] FOREIGN KEY ([status_type_id]) REFERENCES [dbo].[status_type] ([id])
GO
