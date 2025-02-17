import 'package:flutter/material.dart';

class Landing1 extends StatefulWidget {
  const Landing1({super.key});

  @override
  State<Landing1> createState() => _Landing1State();
}

class _Landing1State extends State<Landing1> {

  void nothing () {}

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        leading: IconButton(onPressed: () {
          Navigator.pop(context);
        }
        , icon: Icon(Icons.arrow_back)),

      ),
      backgroundColor: const Color.fromARGB(255, 248, 240, 227),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            //
            // Title
            Text(
              'Is it Legal? 🤔',
              style: TextStyle(
                  fontSize: 40,
                  fontFamily: 'Lato',
                  fontWeight: FontWeight.w700),
            ),

            //
            // Helper Text
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: Text(
                'Find the truth about your wildest ideas!',
                style: TextStyle(
                  fontSize: 13,
                  fontFamily: 'Lato',
                  fontWeight: FontWeight.w600,
                ),
              ),
            ),

            //
            // Search Box
            Container(
              margin: EdgeInsets.only(left: 16, right: 16, top: 8, bottom: 10),
              child: TextField(
                textAlign: TextAlign.start,
                decoration: InputDecoration(
                  contentPadding: EdgeInsets.only(top: 14, bottom: 14),
                  prefixIcon: Icon(Icons.search),
                  hintText: 'Enter your idea...',
                  hintStyle: TextStyle(
                    fontWeight: FontWeight.w400,
                    fontFamily: 'Lato',
                  ),
                  enabledBorder: OutlineInputBorder(
                      borderSide: BorderSide(width: 1),
                      borderRadius: BorderRadius.all(Radius.circular(18))),
                  border: OutlineInputBorder(
                      borderSide: BorderSide(width: 1),
                      borderRadius: BorderRadius.all(Radius.circular(2))),
                ),
              ),
            ),

            SizedBox(height: MediaQuery.of(context).size.height*0.01,),

            //
            // Submit Button
            ElevatedButton(onPressed: nothing, 
              style: ElevatedButton.styleFrom(
                backgroundColor: const Color.fromARGB(255, 136, 118, 111),
                foregroundColor: Colors.white, 
                elevation: 6,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.all(Radius.circular(13),
                  
                  )
                )
              ),
            child: Text(
              'Analyse',
              style: TextStyle(
                fontSize: 18
              ),
              ),
            )
          ],
        ),
      ),
    );
  }
}
