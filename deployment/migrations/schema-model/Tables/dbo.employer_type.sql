CREATE TABLE [dbo].[employer_type]
(
[id] [int] NOT NULL IDENTITY(1, 1),
[name] [varchar] (50) NULL
)
GO
ALTER TABLE [dbo].[employer_type] ADD CONSTRAINT [PK__employer__3213E83FA2970D0C] PRIMARY KEY CLUSTERED ([id])
GO
CREATE NONCLUSTERED INDEX [ix_employer_type_id] ON [dbo].[employer_type] ([id])
GO
