CREATE TABLE [dbo].[employer_type]
(
[id] [int] NOT NULL IDENTITY(1, 1),
[name] [varchar] (50) NULL
)
GO
ALTER TABLE [dbo].[employer_type] ADD CONSTRAINT [PK__employer_type__id] PRIMARY KEY CLUSTERED ([id])
GO
CREATE NONCLUSTERED INDEX [ix_employer_type_id] ON [dbo].[employer_type] ([id])
GO
