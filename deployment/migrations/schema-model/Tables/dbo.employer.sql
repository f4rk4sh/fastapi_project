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
ALTER TABLE [dbo].[employer] ADD CONSTRAINT [PK__employer__3213E83F1D7E874E] PRIMARY KEY CLUSTERED ([id])
GO
CREATE NONCLUSTERED INDEX [ix_employer_edrpou] ON [dbo].[employer] ([edrpou])
GO
CREATE NONCLUSTERED INDEX [ix_employer_id] ON [dbo].[employer] ([id])
GO
ALTER TABLE [dbo].[employer] ADD CONSTRAINT [FK__employer__employ__6F8A7843] FOREIGN KEY ([employer_type_id]) REFERENCES [dbo].[employer_type] ([id])
GO
ALTER TABLE [dbo].[employer] ADD CONSTRAINT [FK__employer__user_i__6E96540A] FOREIGN KEY ([user_id]) REFERENCES [dbo].[user] ([id]) ON DELETE CASCADE
GO
