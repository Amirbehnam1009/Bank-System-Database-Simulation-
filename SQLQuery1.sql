USE [bank]
GO
/** Object:  Table [dbo].[Accounts]    Script Date: 1/29/2024 3:21:58 PM **/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Accounts](
[Id] [bigint] IDENTITY(1,1) NOT NULL,
[NationalCode] [varchar](10) NOT NULL,
[CardNumber] [varchar](16) NOT NULL,
[Sheba] [varchar](24) NOT NULL,
[Money] [bigint] NOT NULL,
CONSTRAINT [PK_Accounts] PRIMARY KEY CLUSTERED
(
[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/** Object:  Table [dbo].[Transactions]    Script Date: 1/29/2024 3:21:58 PM **/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Transactions](
[Id] [bigint] IDENTITY(1,1) NOT NULL,
[From] [bigint] NOT NULL,
[To] [bigint] NOT NULL,
[Money] [bigint] NOT NULL,
[Type] [int] NOT NULL,
[DateTime] [datetime2](7) NOT NULL,
[Status] [bit] NOT NULL,
CONSTRAINT [PK_Transactions_1] PRIMARY KEY CLUSTERED
(
[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/** Object:  Table [dbo].[Users]    Script Date: 1/29/2024 3:21:58 PM **/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Users](
[NationalCode] [varchar](10) NOT NULL,
[Name] [nvarchar](50) NOT NULL,
[LastName] [nvarchar](50) NOT NULL,
[Password] [nvarchar](max) NOT NULL,
CONSTRAINT [PK_Users] PRIMARY KEY CLUSTERED
(
[NationalCode] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
ALTER TABLE [dbo].[Accounts]  WITH CHECK ADD  CONSTRAINT [FK_Users_Accounts] FOREIGN KEY([NationalCode])
REFERENCES [dbo].[Users] ([NationalCode])
GO
ALTER TABLE [dbo].[Accounts] CHECK CONSTRAINT [FK_Users_Accounts]
GO
/** Object:  Trigger [dbo].[UpdateDetails]    Script Date: 1/29/2024 3:21:58 PM **/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

-- create a new trigger
CREATE TRIGGER [dbo].[UpdateDetails]
ON [dbo].[Accounts]
AFTER INSERT
AS
BEGIN  
    SET NOCOUNT ON;
    UPDATE [dbo].[accounts]
    SET  CardNumber = Format(i.Id, '0000000000000000'),
Sheba = Format(i.Id, '000000000000000000000000')
    FROM Inserted i
    WHERE [dbo].[accounts].ID = i.ID
END
GO
ALTER TABLE [dbo].[Accounts] ENABLE TRIGGER [UpdateDetails]
GO