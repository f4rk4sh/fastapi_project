CREATE TABLE [dbo].[employee]
(
[id] [int] NOT NULL IDENTITY(1, 1),
[fullname] [varchar] (100) NULL,
[passport] [varchar] (50) NULL,
[tax_id] [varchar] (50) NULL,
[birth_date] [date] NULL,
[user_id] [int] NULL,
[employer_id] [int] NULL
)
GO
ALTER TABLE [dbo].[employee] ADD CONSTRAINT [PK__employee__id] PRIMARY KEY CLUSTERED ([id])
GO
CREATE NONCLUSTERED INDEX [ix_employee_id] ON [dbo].[employee] ([id])
GO
CREATE NONCLUSTERED INDEX [ix_employee_passport] ON [dbo].[employee] ([passport])
GO
CREATE NONCLUSTERED INDEX [ix_employee_tax_id] ON [dbo].[employee] ([tax_id])
GO
ALTER TABLE [dbo].[employee] ADD CONSTRAINT [FK__employee__employer__id] FOREIGN KEY ([employer_id]) REFERENCES [dbo].[employer] ([id])
GO
ALTER TABLE [dbo].[employee] ADD CONSTRAINT [FK__employee__user__id] FOREIGN KEY ([user_id]) REFERENCES [dbo].[user] ([id]) ON DELETE CASCADE
GO
