ALTER TABLE [dbo].[session] ALTER COLUMN [token] [varchar] (500) NULL
GO

ALTER TABLE [dbo].[session]
ADD
    [expiration_date] [datetime] NULL,
    [user_id] [int] NULL;
GO

ALTER TABLE [dbo].[session] ADD CONSTRAINT [FK__session__user__id] FOREIGN KEY ([user_id]) REFERENCES [dbo].[user] ([id])
GO