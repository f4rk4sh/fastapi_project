CREATE TABLE [dbo].[employer]
(
[id] [int] NOT NULL IDENTITY(1, 1),
[name] [varchar] (100) NULL,
[address] [varchar] (100) NULL,
[edrpou] [varchar] (50) NULL,
[expire_contract_date] [date] NULL,
[salary_date] [date] NULL,
[prepayment_date] [date] NULL,
[user_id] [int] NULL,
[employer_type_id] [int] NULL
)
GO
ALTER TABLE [dbo].[employer] ADD CONSTRAINT [PK__employer__id] PRIMARY KEY CLUSTERED ([id])
GO
CREATE NONCLUSTERED INDEX [ix_employer_edrpou] ON [dbo].[employer] ([edrpou])
GO
CREATE NONCLUSTERED INDEX [ix_employer_id] ON [dbo].[employer] ([id])
GO
ALTER TABLE [dbo].[employer] ADD CONSTRAINT [FK__employer__employer_type__id] FOREIGN KEY ([employer_type_id]) REFERENCES [dbo].[employer_type] ([id])
GO
ALTER TABLE [dbo].[employer] ADD CONSTRAINT [FK__employer__user__id] FOREIGN KEY ([user_id]) REFERENCES [dbo].[user] ([id]) ON DELETE CASCADE
GO
