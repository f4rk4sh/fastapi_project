CREATE TABLE [dbo].[payment_status]
(
[id] [int] NOT NULL IDENTITY(1, 1),
[name] [varchar] (50) NULL
)
GO

ALTER TABLE [dbo].[payment_status] ADD CONSTRAINT [PK__payment_status__id] PRIMARY KEY CLUSTERED ([id])
GO

CREATE NONCLUSTERED INDEX [ix_payment_status_id] ON [dbo].[payment_status] ([id])
GO
