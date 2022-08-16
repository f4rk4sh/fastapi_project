CREATE TABLE [dbo].[session]
(
[id] [int] NOT NULL IDENTITY(1, 1),
[token] [varchar] (100) NULL,
[creation_date] [datetime] NULL
)
GO
ALTER TABLE [dbo].[session] ADD CONSTRAINT [PK__session__id] PRIMARY KEY CLUSTERED ([id])
GO
CREATE NONCLUSTERED INDEX [ix_session_id] ON [dbo].[session] ([id])
GO
