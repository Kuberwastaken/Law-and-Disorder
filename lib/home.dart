import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:law_disorder/games.dart';
import 'package:law_disorder/landing1.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  void nothing() {}

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color.fromARGB(255, 28, 30, 50),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [

            Icon(
              Icons.gavel_rounded,
              color: Colors.white,
              size: 120,
              ),

            SizedBox(height: MediaQuery.of(context).size.height*0.05),

            // TITLE TEXT
            Text(
              'Law & Disorder',
              style: TextStyle(
                color: const Color.fromARGB(255, 242, 226, 2),
                fontSize: 45,
                fontWeight: FontWeight.bold,
                fontFamily: 'Poppins',
              ),
            ),



            // INTRO TEXT
            Padding(
              padding: const EdgeInsets.only(
                  left: 20.0, right: 20, top: 8, bottom: 8),
              child: Text(
                textAlign: TextAlign.center,
                'The hilarious party game where absurd situations meet the Indian Constitution',
                style: TextStyle(
                  color: const Color.fromARGB(255, 255, 255, 255),
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                  fontFamily: 'Lato',
                ),
              ),
            ),

            SizedBox(height: MediaQuery.of(context).size.height*0.03),

            ElevatedButton(
              style: ElevatedButton.styleFrom(
                backgroundColor: const Color.fromARGB(255, 30, 27, 27),
                foregroundColor: Colors.white,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.all(Radius.circular(6),),
                ),
                elevation: 5, 
              ),
              onPressed: () {
                Navigator.push(context, 
                MaterialPageRoute(builder: (context) => GamesPage()));
              },
              child: SizedBox(
                width: MediaQuery.of(context).size.width*0.4,
                child: Row(
                  children: [
                    Padding(
                      padding: const EdgeInsets.all(8.0),
                      child: Text(
                        'Start Playing',
                        style: TextStyle(
                          fontSize: 16,
                        ),
                        ),
                    ),
                    SizedBox(width: MediaQuery.of(context).size.width*0.06,),
                    Icon(Icons.arrow_forward, color: Colors.white,)
                  ],
                ),
              ),
            ),
            


          ],
        ),
      ),
    );
  }
}
