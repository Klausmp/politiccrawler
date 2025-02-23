import {PrismaClient} from '@prisma/client';

const prisma = new PrismaClient();

export const enum Party {
    "CDU",
    "SPD",
    "FDP",
    "Gruene",
    "Linke",
    "AFD"
}

async function main() {
    // Clear existing entries (optional).
    await prisma.party.deleteMany();
    await prisma.channel_Update.deleteMany();
    await prisma.channel.deleteMany();

    // Major German political parties.
    await seedPartys();

    await seedChannel("CDU", "UCKyWIEse3u7ExKfAWuDMVnw", Party.CDU, true);
    await seedChannel("SPD", "UCSmbK1WtpYn2sOGLvSSXkKw", Party.SPD, true);
    await seedChannel("FDP", "UC-sMkrfoQDH-xzMxPNckGFw", Party.FDP, true);
    await seedChannel("Bündnis 90/Die Grünen", "UC7TAA2WYlPfb6eDJCeX4u0w", Party.Gruene, true);
    await seedChannel("Die Linke", "UCA95T5bSGxNOAODBdbR2rYQ", Party.Linke, true);
    await seedChannel("AFD", "UCq2rogaxLtQFrYG3X3KYNww", Party.AFD, true);
    await seedChannel("Ketzer der Neuzeit", "UCjvVn-oLzoY0aZhVvdQPSTQ", Party.AFD);

}

async function seedPartys() {
    const germanParties = [
        {name: "CDU", id: Party.CDU},
        {name: "SPD", id: Party.SPD},
        {name: "FDP", id: Party.FDP},
        {name: "Bündnis 90/Die Grünen", id: Party.Gruene},
        {name: "Die Linke", id: Party.Linke},
        {name: "AfD", id: Party.AFD},
    ];

    await prisma.party.createMany({
        data: germanParties,
        skipDuplicates: true,
    });
}

async function seedChannel(name: string, channel_id: string, partyId: Party, is_party_channel: boolean = false): Promise<void> {
    try {
        const channel = await prisma.channel.create({
            data: {
                name,
                channel_id,
                partyId,
                is_party_channel,
            },
        });
        console.log("Seeded channel:", channel);
    } catch (error) {
        console.error("Error seeding channel:", error);
    }
}


main()
    .then(async () => {
        console.log("Seeding completed successfully.");
        await prisma.$disconnect();
    })
    .catch(async (error) => {
        console.error("Error during seeding:", error);
        await prisma.$disconnect();
        process.exit(1);
    });
