CREATE UNIQUE NONCLUSTERED INDEX [ix_role_name] ON [dbo].[role] ([name])
GO

CREATE UNIQUE NONCLUSTERED INDEX [ix_status_type_name] ON [dbo].[status_type] ([name])
GO

CREATE UNIQUE NONCLUSTERED INDEX [ix_employer_type_name] ON [dbo].[employer_type] ([name])
GO

ALTER TABLE [dbo].[session] ALTER COLUMN [token] [varchar] (400) NULL
GO

ALTER TABLE [dbo].[session]
ADD
    [status] [varchar] (50) NULL,
    [user_id] [int] NULL;
GO

ALTER TABLE [dbo].[session] ADD CONSTRAINT [FK__session__user__id] FOREIGN KEY ([user_id]) REFERENCES [dbo].[user] ([id])
GO