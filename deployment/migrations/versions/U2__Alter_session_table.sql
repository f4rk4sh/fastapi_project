ALTER TABLE [dbo].[session] ALTER COLUMN [token] [varchar] (100) NULL
GO

ALTER TABLE [dbo].[session]
DROP COLUMN [expiration_date], [user_id]
GO

ALTER TABLE [dbo].[session] DROP CONSTRAINT [FK__session__user__id]
GO