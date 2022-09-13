DROP INDEX [ix_role_name] ON [dbo].[role]
GO

DROP INDEX [ix_status_type_name] ON [dbo].[status_type]
GO

DROP INDEX [ix_employer_type_name] ON [dbo].[employer_type]
GO

ALTER TABLE [dbo].[session] ALTER COLUMN [token] [varchar] (100) NULL
GO

ALTER TABLE [dbo].[session]
DROP COLUMN [expiration_date], [user_id]
GO

ALTER TABLE [dbo].[session] DROP CONSTRAINT [FK__session__user__id]
GO