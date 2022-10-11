CREATE TABLE [dbo].[session]
(
[id] [int] NOT NULL IDENTITY(1, 1),
[token] [varchar] (400) NULL,
[creation_date] [datetime] NULL,
[status] [varchar] (50) NULL,
[user_id] [int] NULL
)
GO

ALTER TABLE [dbo].[session] ADD CONSTRAINT [PK__session__id] PRIMARY KEY CLUSTERED ([id])
GO

CREATE NONCLUSTERED INDEX [ix_session_id] ON [dbo].[session] ([id])
GO

ALTER TABLE [dbo].[session] ADD CONSTRAINT [FK__session__user__id] FOREIGN KEY ([user_id]) REFERENCES [dbo].[user] ([id])
GO
