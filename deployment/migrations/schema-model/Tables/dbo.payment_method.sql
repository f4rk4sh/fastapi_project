CREATE TABLE [dbo].[payment_method]
(
[id] [int] NOT NULL IDENTITY(1, 1),
[is_default] [BIT] NULL DEFAULT 0,
[is_active] [BIT] NULL DEFAULT 0,
[employee_id] [int] NULL,
[bank_id] [int] NULL
)
GO

ALTER TABLE [dbo].[payment_method] ADD CONSTRAINT [PK__payment_method__id] PRIMARY KEY CLUSTERED ([id])
GO

CREATE NONCLUSTERED INDEX [ix_payment_method_id] ON [dbo].[payment_method] ([id])
GO

ALTER TABLE [dbo].[payment_method] ADD CONSTRAINT [FK__payment_method__employee__id] FOREIGN KEY ([employee_id]) REFERENCES [dbo].[employee] ([id]) ON DELETE CASCADE
GO

ALTER TABLE [dbo].[payment_method] ADD CONSTRAINT [FK__payment_method__bank__id] FOREIGN KEY ([bank_id]) REFERENCES [dbo].[bank] ([id]) ON DELETE CASCADE
GO
