CREATE TABLE [dbo].[employer_payment_method]
(
[id] [int] NOT NULL IDENTITY(1, 1),
[iban] [varchar] (50) NULL,
[is_active] [BIT] NULL DEFAULT 0,
[creation_date] [datetime] NULL,
[deactivation_date] [date] NULL,
[employer_id] [int] NULL,
[bank_id] [int] NULL
)
GO

ALTER TABLE [dbo].[employer_payment_method] ADD CONSTRAINT [PK__employer_payment_method__id] PRIMARY KEY CLUSTERED ([id])
GO

CREATE NONCLUSTERED INDEX [ix_employer_payment_method_id] ON [dbo].[employer_payment_method] ([id])
GO

ALTER TABLE [dbo].[employer_payment_method] ADD CONSTRAINT [FK__employer_payment_method__employer__id] FOREIGN KEY ([employer_id]) REFERENCES [dbo].[employer] ([id]) ON DELETE CASCADE
GO

ALTER TABLE [dbo].[employer_payment_method] ADD CONSTRAINT [FK__employer_payment_method__bank__id] FOREIGN KEY ([bank_id]) REFERENCES [dbo].[bank] ([id]) ON DELETE CASCADE
GO
