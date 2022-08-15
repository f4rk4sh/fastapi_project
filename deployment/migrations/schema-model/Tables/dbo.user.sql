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
ALTER TABLE [dbo].[user] ADD CONSTRAINT [PK__user__3213E83FEDC8883A] PRIMARY KEY CLUSTERED ([id])
GO
CREATE UNIQUE NONCLUSTERED INDEX [ix_user_email] ON [dbo].[user] ([email])
GO
CREATE NONCLUSTERED INDEX [ix_user_id] ON [dbo].[user] ([id])
GO
ALTER TABLE [dbo].[user] ADD CONSTRAINT [FK__user__role_id__6AC5C326] FOREIGN KEY ([role_id]) REFERENCES [dbo].[role] ([id])
GO
ALTER TABLE [dbo].[user] ADD CONSTRAINT [FK__user__status_typ__6BB9E75F] FOREIGN KEY ([status_type_id]) REFERENCES [dbo].[status_type] ([id])
GO
