import 'package:flutter/material.dart';
import 'package:law_disorder/landing1.dart';

class GamesPage extends StatelessWidget {
  const GamesPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Color(0xFF2F4F4F),


      appBar: AppBar(
        backgroundColor: Colors.transparent,
        leading: IconButton(
          onPressed: () {
            Navigator.pop(context);
          },
          icon: Icon(Icons.arrow_back),
        ),
      ),


      body: Center(
        child: Column(
          // mainAxisAlignment: MainAxisAlignment.center,
          children: [


            // First Card with Gradient
            Container(
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  colors: [
                    Color(0xFF008080),
                    Color(0xFF00008B)
                  ], // Teal to Dark Blue
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                ),
                borderRadius:
                    BorderRadius.circular(15), // Rounded corners for card
              ),


              padding: EdgeInsets.all(8),
              height: MediaQuery.of(context).size.height * 0.35,
              width: MediaQuery.of(context).size.width * 0.90,


              child: Card(
                color: Color(0xFFF5F5DC),
                elevation: 8,
                shape: RoundedRectangleBorder(
                  borderRadius:
                      BorderRadius.circular(15), // Rounded corners for card
                ),
                child: Center(
                  child: Column(
                    children: [

                      Text(
                        'Is it Legal ',
                        style: TextStyle(
                          fontSize: 24,
                          fontWeight: FontWeight.bold,
                          color: const Color.fromARGB(255, 0, 0, 0),
                        ),
                      ),
                      ElevatedButton(
                        style: ElevatedButton.styleFrom(
                          backgroundColor:
                              const Color.fromARGB(255, 30, 27, 27),
                          foregroundColor: Colors.white,
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.all(
                              Radius.circular(6),
                            ),
                          ),
                          elevation: 5,
                        ),
                        onPressed: () {
                          Navigator.push(
                              context,
                              MaterialPageRoute(
                                  builder: (context) => Landing1()));
                        },
                        child: SizedBox(
                          width: MediaQuery.of(context).size.width * 0.2,
                          child: Padding(
                            padding: const EdgeInsets.all(8.0),
                            child: Center(
                              child: Text(
                                'Play Now',
                                style: TextStyle(
                                  fontSize: 14,
                                ),
                              ),
                            ),
                          ),
                        ),
                      ),

                    ],
                  ),
                ),
              ),
            ),

            SizedBox(height: 20),

            // Second Card with Gradient
            Container(
              margin: EdgeInsets.only(left: 10, right: 10),
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  colors: [
                    Color(0xFFFF7F50),
                    Color(0xFFE91E63)
                  ], // Coral to Pink
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                ),
                borderRadius:
                    BorderRadius.circular(15), // Rounded corners for card
              ),
              padding: EdgeInsets.all(8),
              height: MediaQuery.of(context).size.height * 0.35,
              width: MediaQuery.of(context).size.width * 0.90,
              child: Card(
                color: const Color(0xFFF5F5DC),
                elevation: 8,
                shape: RoundedRectangleBorder(
                  borderRadius:
                      BorderRadius.circular(15), // Rounded corners for card
                ),
                child: Center(
                  child: Column(
                    children: [
                      Text(
                        'Quiz Game',
                        style: TextStyle(
                          fontSize: 24,
                          fontWeight: FontWeight.bold,
                          color: const Color.fromARGB(255, 0, 0, 0),
                        ),
                      ),
                      ElevatedButton(
                        style: ElevatedButton.styleFrom(
                          backgroundColor:
                              const Color.fromARGB(255, 30, 27, 27),
                          foregroundColor: Colors.white,
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.all(
                              Radius.circular(6),
                            ),
                          ),
                          elevation: 5,
                        ),
                        onPressed: () {
                          Navigator.push(
                              context,
                              MaterialPageRoute(
                                  builder: (context) => Landing1()));
                        },
                        child: SizedBox(
                          width: MediaQuery.of(context).size.width * 0.2,
                          child: Padding(
                            padding: const EdgeInsets.all(8.0),
                            child: Center(
                              child: Text(
                                'Play Now',
                                style: TextStyle(
                                  fontSize: 14,
                                ),
                              ),
                            ),
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
