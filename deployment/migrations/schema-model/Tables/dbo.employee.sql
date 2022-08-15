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
ALTER TABLE [dbo].[employee] ADD CONSTRAINT [PK__employee__3213E83FD35367B1] PRIMARY KEY CLUSTERED ([id])
GO
CREATE NONCLUSTERED INDEX [ix_employee_id] ON [dbo].[employee] ([id])
GO
CREATE NONCLUSTERED INDEX [ix_employee_passport] ON [dbo].[employee] ([passport])
GO
CREATE NONCLUSTERED INDEX [ix_employee_tax_id] ON [dbo].[employee] ([tax_id])
GO
ALTER TABLE [dbo].[employee] ADD CONSTRAINT [FK__employee__employ__735B0927] FOREIGN KEY ([employer_id]) REFERENCES [dbo].[employer] ([id])
GO
ALTER TABLE [dbo].[employee] ADD CONSTRAINT [FK__employee__user_i__7266E4EE] FOREIGN KEY ([user_id]) REFERENCES [dbo].[user] ([id]) ON DELETE CASCADE
GO
